from typing import List, Optional

from langflow_base.components.vectorstores.base.model import LCVectorStoreComponent
from langflow_base.components.vectorstores.MongoDBAtlasVector import MongoDBAtlasComponent
from langflow_base.field_typing import Embeddings, NestedDict, Text
from langflow_base.schema import Record


class MongoDBAtlasSearchComponent(MongoDBAtlasComponent, LCVectorStoreComponent):
    display_name = "MongoDB Atlas Search"
    description = "Search a MongoDB Atlas Vector Store for similar documents."

    def build_config(self):
        return {
            "search_type": {
                "display_name": "Search Type",
                "options": ["Similarity", "MMR"],
            },
            "input_value": {"display_name": "Input"},
            "embedding": {"display_name": "Embedding"},
            "collection_name": {"display_name": "Collection Name"},
            "db_name": {"display_name": "Database Name"},
            "index_name": {"display_name": "Index Name"},
            "mongodb_atlas_cluster_uri": {"display_name": "MongoDB Atlas Cluster URI"},
            "search_kwargs": {"display_name": "Search Kwargs", "advanced": True},
        }

    def build(  # type: ignore[override]
        self,
        input_value: Text,
        search_type: str,
        embedding: Embeddings,
        collection_name: str = "",
        db_name: str = "",
        index_name: str = "",
        mongodb_atlas_cluster_uri: str = "",
        search_kwargs: Optional[NestedDict] = None,
    ) -> List[Record]:
        search_kwargs = search_kwargs or {}
        vector_store = super().build(
            connection_string=mongodb_atlas_cluster_uri,
            namespace=f"{db_name}.{collection_name}",
            embedding=embedding,
            index_name=index_name,
        )
        if not vector_store:
            raise ValueError("Failed to create MongoDB Atlas Vector Store")
        return self.search_with_vector_store(
            vector_store=vector_store, input_value=input_value, search_type=search_type
        )
