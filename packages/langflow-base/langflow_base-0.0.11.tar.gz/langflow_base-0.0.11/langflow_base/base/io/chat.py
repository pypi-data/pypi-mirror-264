import warnings
from typing import Optional, Union

from langflow_base.interface.custom.custom_component import CustomComponent
from langflow_base.field_typing import Text
from langflow_base.memory import add_messages
from langflow_base.schema import Record


class ChatComponent(CustomComponent):
    display_name = "Chat Component"
    description = "Use as base for chat components."

    def build_config(self):
        return {
            "input_value": {
                "input_types": ["Text"],
                "display_name": "Message",
                "multiline": True,
            },
            "sender": {
                "options": ["Machine", "User"],
                "display_name": "Sender Type",
            },
            "sender_name": {"display_name": "Sender Name"},
            "session_id": {
                "display_name": "Session ID",
                "info": "If provided, the message will be stored in the memory.",
                "advanced": True,
            },
            "return_record": {
                "display_name": "Return Record",
                "info": "Return the message as a record containing the sender, sender_name, and session_id.",
            },
        }

    def store_message(
        self,
        message: Union[str, Text, Record],
        session_id: Optional[str] = None,
        sender: Optional[str] = None,
        sender_name: Optional[str] = None,
    ) -> list[Record]:
        if not message:
            warnings.warn("No message provided.")
            return []

        if not session_id or not sender or not sender_name:
            raise ValueError("All of session_id, sender, and sender_name must be provided.")
        if isinstance(message, Record):
            record = message
            record.data.update(
                {
                    "session_id": session_id,
                    "sender": sender,
                    "sender_name": sender_name,
                }
            )
        else:
            record = Record(
                data={
                    "text": message,
                    "session_id": session_id,
                    "sender": sender,
                    "sender_name": sender_name,
                },
            )

        self.status = record
        records = add_messages([record])
        return records[0]

    def build(
        self,
        sender: Optional[str] = "User",
        sender_name: Optional[str] = "User",
        input_value: Optional[str] = None,
        session_id: Optional[str] = None,
        return_record: Optional[bool] = False,
    ) -> Union[Text, Record]:
        input_value_record: Optional[Record] = None
        if return_record:
            if isinstance(input_value, Record):
                # Update the data of the record
                input_value.data["sender"] = sender
                input_value.data["sender_name"] = sender_name
                input_value.data["session_id"] = session_id
            else:
                input_value_record = Record(
                    text=input_value,
                    data={
                        "sender": sender,
                        "sender_name": sender_name,
                        "session_id": session_id,
                    },
                )
        if not input_value:
            input_value = ""
        if return_record and input_value_record:
            result: Union[Text, Record] = input_value_record
        else:
            result = input_value
        self.status = result
        if session_id:
            self.store_message(result, session_id, sender, sender_name)
        return result
