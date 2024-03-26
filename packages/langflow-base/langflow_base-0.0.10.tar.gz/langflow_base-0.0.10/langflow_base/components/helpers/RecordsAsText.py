from langflow_base.interface.custom.custom_component import CustomComponent

from langflow_base.field_typing import Text
from langflow_base.helpers.record import records_to_text
from langflow_base.schema import Record


class RecordsAsTextComponent(CustomComponent):
    display_name = "Records to Text"
    description = "Converts Records into single piece of text using a template."

    def build_config(self):
        return {
            "records": {
                "display_name": "Records",
                "info": "The records to convert to text.",
            },
            "template": {
                "display_name": "Template",
                "info": "The template to use for formatting the records. It can contain the keys {text}, {data} or any other key in the Record.",
            },
        }

    def build(
        self,
        records: list[Record],
        template: str = "Text: {text}\nData: {data}",
    ) -> Text:
        if not records:
            return ""
        if isinstance(records, Record):
            records = [records]

        result_string = records_to_text(template, records)
        self.status = result_string
        return result_string
