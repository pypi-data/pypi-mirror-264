from typing import List

from langflow_base.interface.custom.custom_component import CustomComponent

from langflow_base.schema import Record
from langflow_base.utils.constants import LOADERS_INFO


class FileLoaderComponent(CustomComponent):
    display_name: str = "File Loader"
    description: str = "Generic File Loader"

    def build_config(self):
        loader_options = ["Automatic"] + [loader_info["name"] for loader_info in LOADERS_INFO]

        file_types = []
        suffixes = []

        for loader_info in LOADERS_INFO:
            if "allowedTypes" in loader_info:
                file_types.extend(loader_info["allowedTypes"])
                suffixes.extend([f".{ext}" for ext in loader_info["allowedTypes"]])

        return {
            "file_path": {
                "display_name": "File Path",
                "required": True,
                "field_type": "file",
                "file_types": [
                    "json",
                    "txt",
                    "csv",
                    "jsonl",
                    "html",
                    "htm",
                    "conllu",
                    "enex",
                    "msg",
                    "pdf",
                    "srt",
                    "eml",
                    "md",
                    "mdx",
                    "pptx",
                    "docx",
                ],
                "suffixes": [
                    ".json",
                    ".txt",
                    ".csv",
                    ".jsonl",
                    ".html",
                    ".htm",
                    ".conllu",
                    ".enex",
                    ".msg",
                    ".pdf",
                    ".srt",
                    ".eml",
                    ".md",
                    ".mdx",
                    ".pptx",
                    ".docx",
                ],
                # "file_types" : file_types,
                # "suffixes": suffixes,
            },
            "loader": {
                "display_name": "Loader",
                "is_list": True,
                "required": True,
                "options": loader_options,
                "value": "Automatic",
            },
            "code": {"show": False},
        }

    def build(self, file_path: str, loader: str) -> List[Record]:
        file_type = file_path.split(".")[-1]

        # Map the loader to the correct loader class
        selected_loader_info = None
        for loader_info in LOADERS_INFO:
            if loader_info["name"] == loader:
                selected_loader_info = loader_info
                break

        if selected_loader_info is None and loader != "Automatic":
            raise ValueError(f"Loader {loader} not found in the loader info list")

        if loader == "Automatic":
            # Determine the loader based on the file type
            default_loader_info = None
            for info in LOADERS_INFO:
                if "defaultFor" in info and file_type in info["defaultFor"]:
                    default_loader_info = info
                    break

            if default_loader_info is None:
                raise ValueError(f"No default loader found for file type: {file_type}")

            selected_loader_info = default_loader_info
        if isinstance(selected_loader_info, dict):
            loader_import: str = selected_loader_info["import"]
        else:
            raise ValueError(f"Loader info for {loader} is not a dict\nLoader info:\n{selected_loader_info}")
        module_name, class_name = loader_import.rsplit(".", 1)

        try:
            # Import the loader class
            loader_module = __import__(module_name, fromlist=[class_name])
            loader_instance = getattr(loader_module, class_name)
        except ImportError as e:
            raise ValueError(f"Loader {loader} could not be imported\nLoader info:\n{selected_loader_info}") from e

        result = loader_instance(file_path=file_path)
        docs = result.load()
        return self.to_records(docs)
