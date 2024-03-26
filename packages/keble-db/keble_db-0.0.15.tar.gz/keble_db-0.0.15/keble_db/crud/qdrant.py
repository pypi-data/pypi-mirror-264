from typing import Generic, List, Optional, Type, TypeVar, Union, Sequence, Tuple
from pydantic import BaseModel
from ..schemas import QueryBase
from .sql_util import parse_query_for_first, parse_query_for_list
from sqlmodel import Session, select
from sqlalchemy import func
from qdrant_client import QdrantClient, models as qdrant_models
from qdrant_client.conversions import common_types as qdrant_types
from .qdrant_util import cleanse_query_for_search

ModelType = TypeVar("ModelType", bound=BaseModel)
VectorModelType = TypeVar("VectorModelType", bound=BaseModel)


class Record(qdrant_types.Record):
    payload: ModelType
    score: Optional[float] = None


class QdrantCRUDBase(Generic[ModelType, VectorModelType]):

    def __init__(self, model: Type[ModelType], vector_model: Type[VectorModelType], collection: str):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD) in Qdrant

        **Parameters**
        * `model`: A Qdrant Alchemy model class
        """
        self.model: Type[ModelType] = model
        self.vector_model: Type[VectorModelType] = vector_model
        self.collection = collection

    def __is_result_success(self, result: qdrant_types.UpdateResult):
        return result.status.lower() == qdrant_models.UpdateStatus.COMPLETED.value.lower()

    def get_multi_records_by_ids(
            self,
            client: QdrantClient,
            *,
            _ids: Sequence[qdrant_types.PointId]
    ) -> List[Record]:
        records = client.retrieve(
            self.collection,
            ids=_ids,
        )
        return [Record(**record.model_dump(exclude={"payload"}), payload=record.payload) for record in records]

    def get_multi_by_ids(
            self,
            client: QdrantClient,
            *,
            _ids: Sequence[qdrant_types.PointId]
    ) -> List[ModelType]:
        records = self.get_multi_records_by_ids(client, _ids=_ids)
        return [r.payload for r in records]

    def first_record_by_id(
            self,
            client: QdrantClient,
            *,
            _id: qdrant_types.PointId
    ) -> Optional[Record]:
        records: List[Record] = self.get_multi_records_by_ids(client, _ids=[_id])
        if len(records) < 1: return None
        return records[0]

    def first_by_id(
            self,
            client: QdrantClient,
            *,
            _id: qdrant_types.PointId
    ) -> Optional[ModelType]:
        record = self.first_record_by_id(client, _id=_id)
        if record is not None: return record.payload

    def search(self, client: QdrantClient, *, vector: List[float], vector_key: str, query: Optional[QueryBase] = None,
               score_threshold: float = 0.76
               # 0.76 ~ 0.8 is a decent threshold base on our test, among different languages
               ) -> List[Record]:
        filter_ = cleanse_query_for_search(query)
        scored_points: List[qdrant_types.ScoredPoint] = client.search(
            self.collection,
            query_filter=filter_,
            query_vector=(vector_key, vector),
            limit=query.limit,
            offset=query.offset,
            score_threshold=score_threshold
        )
        return [Record(**sp.model_dump(include={"score", "payload", "vector", "shard_key", "id"})) for sp in
                scored_points]

    def create(
            self,
            client: QdrantClient,
            vector: VectorModelType,
            payload: ModelType,
            _id: qdrant_types.PointId
    ) -> bool:
        vector_dict = vector.model_dump()
        _, status = client.upsert(
            collection_name=self.collection,
            points=[
                qdrant_models.PointStruct(
                    id=_id,
                    vector=vector_dict,
                    payload=payload.model_dump(),
                )
            ]
        )
        status = status[1] if isinstance(status, tuple) and len(status) > 1 else status
        return str(status).lower() == qdrant_models.UpdateStatus.COMPLETED.value.lower()

    def create_multi(
            self,
            client: QdrantClient,
            *,
            payloads_and_vectors: List[Tuple[str, ModelType, VectorModelType]]
    ) -> bool:

        points: List[qdrant_models.PointStruct] = [
            qdrant_models.PointStruct(
                id=_id,
                vector=vector.model_dump(),
                payload=payload.model_dump(),
            )
            for _id, payload, vector in payloads_and_vectors
        ]

        _, status = client.upsert(
            collection_name=self.collection,
            points=points,
        )
        status = status[1] if isinstance(status, tuple) and len(status) > 1 else status
        return str(status).lower() == qdrant_models.UpdateStatus.COMPLETED.value.lower()

    def delete(
            self,
            client: QdrantClient,
            *,
            _id: qdrant_types.PointId,
    ) -> bool:
        update_result: qdrant_types.UpdateResult = client.delete(
            self.collection,
            points_selector=[_id]
        )
        return self.__is_result_success(update_result)

    def update_payload(self, client: QdrantClient, *, _id: qdrant_types.PointId, payload: ModelType):
        old_payload = self.first_by_id(client, _id=_id)
        if old_payload is not None:
            obj_dict = old_payload.model_dump()
            obj_dict.update(payload.model_dump())
            res = client.set_payload(
                collection_name=self.collection,
                payload=self.model(**obj_dict).model_dump(),
                points=[_id]
            )
            return self.__is_result_success(res)
        return False

    def update_vector(self, client: QdrantClient, *, _id: qdrant_types.PointId, vector: VectorModelType) -> bool:
        res = client.update_vectors(
            collection_name=self.collection,
            points=[
                qdrant_models.PointVectors(
                    id=_id,
                    vector=vector.model_dump()
                )
            ],
        )
        return self.__is_result_success(res)