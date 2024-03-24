# coding: utf-8

"""
    FINBOURNE Luminesce Web API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, StrictInt, StrictStr

class OptionsXml(BaseModel):
    """
    Additional options applicable to the given SourceType  # noqa: E501
    """
    column_types: Optional[StrictStr] = Field(None, alias="columnTypes", description="Column types (comma delimited list of: '{types}', some columns may be left blank while others are specified)")
    infer_type_row_count: Optional[StrictInt] = Field(None, alias="inferTypeRowCount", description="If non-zero and 'types' is not specified (or not specified for some columns) this will look through N rows to attempt to work out the column types for columns not pre-specified")
    values_to_make_null: Optional[StrictStr] = Field(None, alias="valuesToMakeNull", description="Regex of values to map to 'null' in the returned data.")
    column_names: Optional[StrictStr] = Field(None, alias="columnNames", description="Column Names either overrides the header row or steps in when there is no header row (comma delimited list)")
    node_path: Optional[StrictStr] = Field(None, alias="nodePath", description="XPath query that selects the nodes to map to rows")
    namespaces: Optional[StrictStr] = Field(None, description="Selected prefix(es) and namespace(s):prefix1=namespace1-uri1,prefix2=namespace2-uri2,...prefixN=namespaceN-uriN")
    __properties = ["columnTypes", "inferTypeRowCount", "valuesToMakeNull", "columnNames", "nodePath", "namespaces"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> OptionsXml:
        """Create an instance of OptionsXml from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if column_types (nullable) is None
        # and __fields_set__ contains the field
        if self.column_types is None and "column_types" in self.__fields_set__:
            _dict['columnTypes'] = None

        # set to None if values_to_make_null (nullable) is None
        # and __fields_set__ contains the field
        if self.values_to_make_null is None and "values_to_make_null" in self.__fields_set__:
            _dict['valuesToMakeNull'] = None

        # set to None if column_names (nullable) is None
        # and __fields_set__ contains the field
        if self.column_names is None and "column_names" in self.__fields_set__:
            _dict['columnNames'] = None

        # set to None if node_path (nullable) is None
        # and __fields_set__ contains the field
        if self.node_path is None and "node_path" in self.__fields_set__:
            _dict['nodePath'] = None

        # set to None if namespaces (nullable) is None
        # and __fields_set__ contains the field
        if self.namespaces is None and "namespaces" in self.__fields_set__:
            _dict['namespaces'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OptionsXml:
        """Create an instance of OptionsXml from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OptionsXml.parse_obj(obj)

        _obj = OptionsXml.parse_obj({
            "column_types": obj.get("columnTypes"),
            "infer_type_row_count": obj.get("inferTypeRowCount"),
            "values_to_make_null": obj.get("valuesToMakeNull"),
            "column_names": obj.get("columnNames"),
            "node_path": obj.get("nodePath"),
            "namespaces": obj.get("namespaces")
        })
        return _obj
