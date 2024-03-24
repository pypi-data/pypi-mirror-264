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
from pydantic import BaseModel, Field, StrictStr
from luminesce.models.data_type import DataType
from luminesce.models.expression_with_alias import ExpressionWithAlias

class MappableField(BaseModel):
    """
    Information about a field that can be designed on (regardless if it currently is)  Kind of a \"mini-available catalog entry\"  # noqa: E501
    """
    name: Optional[StrictStr] = Field(None, description="Name of the field in need of mapping (The field name from within the Table Parameter itself)")
    type: Optional[DataType] = None
    description: Optional[StrictStr] = Field(None, description="Description of the field (just for rendering to the user)")
    display_name: Optional[StrictStr] = Field(None, alias="displayName", description="Display Name of the field (just for rendering to the user)")
    sample_values: Optional[StrictStr] = Field(None, alias="sampleValues", description="Example values for the field (just for rendering to the user)")
    allowed_values: Optional[StrictStr] = Field(None, alias="allowedValues", description="Any set of exactly allowed values for the field (perhaps just for rendering to the user, if nothing else)")
    mandatory_for_actions: Optional[StrictStr] = Field(None, alias="mandatoryForActions", description="Which `Actions` is this mandatory for? If any (and potentially when), perhaps just for rendering to the user, if nothing else")
    mapping: Optional[ExpressionWithAlias] = None
    __properties = ["name", "type", "description", "displayName", "sampleValues", "allowedValues", "mandatoryForActions", "mapping"]

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
    def from_json(cls, json_str: str) -> MappableField:
        """Create an instance of MappableField from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of mapping
        if self.mapping:
            _dict['mapping'] = self.mapping.to_dict()
        # set to None if name (nullable) is None
        # and __fields_set__ contains the field
        if self.name is None and "name" in self.__fields_set__:
            _dict['name'] = None

        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        # set to None if display_name (nullable) is None
        # and __fields_set__ contains the field
        if self.display_name is None and "display_name" in self.__fields_set__:
            _dict['displayName'] = None

        # set to None if sample_values (nullable) is None
        # and __fields_set__ contains the field
        if self.sample_values is None and "sample_values" in self.__fields_set__:
            _dict['sampleValues'] = None

        # set to None if allowed_values (nullable) is None
        # and __fields_set__ contains the field
        if self.allowed_values is None and "allowed_values" in self.__fields_set__:
            _dict['allowedValues'] = None

        # set to None if mandatory_for_actions (nullable) is None
        # and __fields_set__ contains the field
        if self.mandatory_for_actions is None and "mandatory_for_actions" in self.__fields_set__:
            _dict['mandatoryForActions'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> MappableField:
        """Create an instance of MappableField from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return MappableField.parse_obj(obj)

        _obj = MappableField.parse_obj({
            "name": obj.get("name"),
            "type": obj.get("type"),
            "description": obj.get("description"),
            "display_name": obj.get("displayName"),
            "sample_values": obj.get("sampleValues"),
            "allowed_values": obj.get("allowedValues"),
            "mandatory_for_actions": obj.get("mandatoryForActions"),
            "mapping": ExpressionWithAlias.from_dict(obj.get("mapping")) if obj.get("mapping") is not None else None
        })
        return _obj
