"""Module for class represent Flywheel file object."""
import typing as t
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class File:
    """Class representing metadata of a Flywheel file.

    The SDK and config.json represent files differently. This object
    holds all the metadata associated with a file in a predictable manner
    and allows for converting from SDK or config.json file representations.

    Attributes:
        name (str): File name.
        parent_type (str): Container type of file's parent.
        modality (str): File modality.
        fw_type (str): Flywheel file type.
        mimetype (str): File mimetype.
        classification (Dict[str, List[str]]): Classification dictionary.
        tags (List[str]): List of tags.
        info (dict): Custom information dict.
        local_path (Optional[Path]): Local path to file
        parents (Dict[str, str]): File parents.
        zip_member_count (Optional[int]): File zip member count.
        version (Optional[int]): File version.
        file_id (Optional[str]): File id.
        size (Optional[int]): File size in bytes.
    """

    name: str
    parent_type: str
    modality: str = ""
    fw_type: str = ""
    mimetype: str = ""
    classification: t.Dict[str, t.List[str]] = field(default_factory=dict)
    tags: t.List[str] = field(default_factory=list)
    info: dict = field(default_factory=dict)
    local_path: t.Optional[Path] = None
    parents: t.Dict[str, str] = field(default_factory=dict)
    zip_member_count: t.Optional[int] = None
    version: t.Optional[int] = None
    file_id: t.Optional[str] = None
    size: t.Optional[int] = None
    parent_id: t.Optional[str] = None

    @classmethod
    def from_config(cls, file_: dict) -> "File":
        """Create a File object from a config.json input dictionary.

        Args:
            file_ (dict): Config.json dictionary representing the file.
        """
        # file_ passed in from config.json
        obj = file_.get("object", {})
        return cls(
            file_.get("location", {}).get("name", ""),
            file_.get("hierarchy", {}).get("type", ""),
            parent_id=file_.get("hierarchy", {}).get("id", None),
            modality=obj.get("modality", ""),
            fw_type=obj.get("type", ""),
            mimetype=obj.get("mimetype", ""),
            classification=obj.get("classification", {}),
            tags=obj.get("tags", []),
            info=obj.get("info", {}),
            local_path=file_.get("location", {}).get("path", None),
            zip_member_count=obj.get("zip_member_count", None),
            version=obj.get("version", None),
            file_id=obj.get("file_id", None),
            size=obj.get("size", None),
        )

    @classmethod
    def from_sdk(cls, file_: dict) -> "File":
        """Create a File from an SDK "file".

        Args:
            file_ (dict): SDK "file" object
        """
        parent_type = file_.get("parent_ref", {}).get("type", "")
        return cls(
            file_.get("name", ""),
            parent_type,
            modality=file_.get("modality", ""),
            fw_type=file_.get("type", ""),
            mimetype=file_.get("mimetype", ""),
            classification=file_.get("classification", {}),
            tags=file_.get("tags", []),
            info=file_.get("info", {}),
            parents=file_.get("parents", {}),
            zip_member_count=file_.get("zip_member_count", None),
            version=file_.get("version", None),
            file_id=file_.get("file_id", None),
            size=file_.get("size", None),
            parent_id=file_.get("parents", {}).get(parent_type, ""),
        )
