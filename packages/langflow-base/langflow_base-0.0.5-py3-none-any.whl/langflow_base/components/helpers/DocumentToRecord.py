from typing import List

from langchain_core.documents import Document

from langflow_base.interface.custom.custom_component import CustomComponent

from langflow_base.schema import Record


class DocumentToRecordComponent(CustomComponent):
    display_name = "Documents to Records"
    description = "Convert documents to records."

    field_config = {
        "documents": {"display_name": "Documents"},
    }

    def build(self, documents: List[Document]) -> List[Record]:
        if isinstance(documents, Document):
            documents = [documents]
        records = [Record.from_document(document) for document in documents]
        self.status = records
        return records
