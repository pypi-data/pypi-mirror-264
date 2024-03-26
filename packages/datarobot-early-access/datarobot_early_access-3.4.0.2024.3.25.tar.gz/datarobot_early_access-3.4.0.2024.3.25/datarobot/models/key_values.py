#
# Copyright 2021-2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import List, Optional, Set

import trafaret as t

from datarobot._compat import String
from datarobot.enums import KeyValueCategory, KeyValueEntityType, KeyValueType
from datarobot.models.api_object import APIObject
from datarobot.utils.pagination import unpaginate


class KeyValue(APIObject):
    """A DataRobot Key-Value.

    .. versionadded:: v3.4

    Attributes
    ----------
    id: str
        ID of the Key-Value
    created_at: str
        creation time of the Key-Value
    entity_id: str
        ID of the related Entity
    entity_type: KeyValueEntityType
        type of the related Entity
    name: str
        Key-Value name
    value: str
        Key-Value value
    numeric_value: float
        Key-Value numeric value
    boolean_value: bool
        Key-Value boolean value
    value_type: KeyValueType
        Key-Value type
    description: str
        Key-Value description
    creator_id: str
        ID of the user who created the Key-Value
    creator_name: str
        ID of the user who created the Key-Value
    category: KeyValueCategory
        Key-Value category
    artifact_size: int
        size in bytes of associated image, if applicable
    original_file_name: str
        name of uploaded original image or dataset file
    is_editable: bool
        true if a user with permissions can edit or delete
    is_dataset_missing: bool
        true if the key-value type is "dataset" and its dataset is not visible to the user
    error_message: str
        additional information if "isDataSetMissing" is true. Blank if there are no errors
    """

    _path = "keyValues/"

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("created_at"): String(),
            t.Key("entity_id"): String(),
            t.Key("entity_type"): t.Enum(*[e.value for e in KeyValueEntityType]),
            t.Key("name"): String(),
            t.Key("value"): String(),
            t.Key("numeric_value"): t.Float(),
            t.Key("boolean_value", optional=True, default=False): t.Bool(),
            t.Key("value_type"): t.Enum(*[e.value for e in KeyValueType]),
            t.Key("description"): String(allow_blank=True),
            t.Key("creator_id"): String(),
            t.Key("creator_name"): String(),
            t.Key("category"): t.Enum(*[e.value for e in KeyValueCategory]),
            t.Key("artifact_size"): t.Int(),
            t.Key("original_file_name"): String(allow_blank=True),
            t.Key("is_editable"): t.Bool(),
            t.Key("is_dataset_missing"): t.Bool(),
            t.Key("error_message"): String(allow_blank=True),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(
        self,
        id: str,
        created_at: str,
        entity_id: str,
        entity_type: KeyValueEntityType,
        name: str,
        value: str,
        numeric_value: float,
        boolean_value: bool,
        value_type: KeyValueType,
        description: str,
        creator_id: str,
        creator_name: str,
        category: KeyValueCategory,
        artifact_size: int,
        original_file_name: str,
        is_editable: bool,
        is_dataset_missing: bool,
        error_message: str,
    ) -> None:
        self.id = id
        self.created_at = created_at
        self.entity_id = entity_id
        self.entity_type = KeyValueEntityType(entity_type)
        self.name = name
        self.value = value
        self.numeric_value = numeric_value
        self.boolean_value = boolean_value
        self.value_type = KeyValueType(value_type)
        self.description = description
        self.creator_id = creator_id
        self.creator_name = creator_name
        self.category = KeyValueCategory(category)
        self.artifact_size = artifact_size
        self.original_file_name = original_file_name
        self.is_editable = is_editable
        self.is_dataset_missing = is_dataset_missing
        self.error_message = error_message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name or self.id!r})"

    def _update_values(self, new_response: KeyValue) -> None:
        fields: Set[str] = self._fields()  # type: ignore[no-untyped-call]
        for attr in fields:
            new_value = getattr(new_response, attr)
            setattr(self, attr, new_value)

    @classmethod
    def _key_value_path(cls, key_value_id: str) -> str:
        return f"{cls._path}{key_value_id}/"

    @classmethod
    def get(cls, key_value_id: str) -> KeyValue:
        """Get Key-Value by id.

        .. versionadded:: v3.4

        Parameters
        ----------
        key_value_id: str
            ID of the Key-Value

        Returns
        -------
        KeyValue
            retrieved Key-Value

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        path = cls._key_value_path(key_value_id)
        return cls.from_location(path)

    @classmethod
    def list(cls, entity_id: str, entity_type: KeyValueEntityType) -> List[KeyValue]:
        """List Key-Values.

        .. versionadded:: v3.4

        Parameters
        ----------
        entity_id: str
            ID of the related Entity
        entity_type: KeyValueEntityType
            type of the related Entity

        Returns
        -------
        List[KeyValue]
            a list of Key-Values

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        data = unpaginate(
            cls._path,
            {"entityId": entity_id, "entityType": entity_type.value},
            cls._client,
        )
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def create(
        cls,
        entity_id: str,
        entity_type: KeyValueEntityType,
        name: str,
        category: KeyValueCategory,
        value_type: KeyValueType,
        value: Optional[str] = None,
        numeric_value: Optional[float] = None,
        boolean_value: Optional[bool] = None,
        description: Optional[str] = None,
    ) -> KeyValue:
        """Create a Key-Value.

        .. versionadded:: v3.4

        Parameters
        ----------
        entity_id: str
            ID of the associated resource
        entity_type: KeyValueEntityType
            type of the associated resource
        name: str
            name of the Key-Value. Cannot contain: { } ; |
        category: KeyValueCategory
            category of the Key-Value
        value_type: KeyValueType
            type of the Key-Value value
        value: Optional[str]
            value of non-numeric Key-Value
        numeric_value: Optional[float]
            value of numeric type Key-Value
        boolean_value: Optional[bool]
            value of boolean type Key-Value
        description: Optional[str]
            description of the Key-Value

        Returns
        -------
        KeyValue
            created Key-Value

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        response = cls._client.post(
            cls._path,
            data={
                "entityId": entity_id,
                "entityType": entity_type.value,
                "name": name,
                "category": category.value,
                "value_type": value_type.value,
                "value": value,
                "numericValue": numeric_value,
                "booleanValue": boolean_value,
                "description": description,
            },
        )

        return cls.get(response.json()["id"])

    def update(
        self,
        entity_id: str,
        entity_type: KeyValueEntityType,
        name: str,
        category: KeyValueCategory,
        value_type: KeyValueType,
        value: Optional[str] = None,
        numeric_value: Optional[float] = None,
        boolean_value: Optional[bool] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> None:
        """Update Key-Value.

        .. versionadded:: v3.4

        Parameters
        ----------
        entity_id: str
            ID of the associated resource
        entity_type: KeyValueEntityType
            type of the associated resource
        name: str
            name of the Key-Value. Cannot contain: { } ; |
        category: KeyValueCategory
            category of the Key-Value
        value_type: KeyValueType
            type of the Key-Value value
        value: Optional[str]
            value of non-numeric Key-Value
        numeric_value: Optional[float]
            value of numeric type Key-Value
        boolean_value: Optional[bool]
            value of boolean type Key-Value
        description: Optional[str]
            description of the Key-Value
        comment: Optional[str]
            user comment explaining the change

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        response = self._client.patch(
            self._key_value_path(self.id),
            data={
                "entityId": entity_id,
                "entityType": entity_type.value,
                "name": name,
                "category": category.value,
                "valueType": value_type.value,
                "value": value,
                "numericValue": numeric_value,
                "booleanValue": boolean_value,
                "description": description,
                "comment": comment,
            },
        )

        data = response.json()
        new_version = self.from_server_data(data)
        self._update_values(new_version)

    def refresh(self) -> None:
        """Update Key-Value with the latest data from server.

        .. versionadded:: v3.4

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """

        new_object = self.get(self.id)
        self._update_values(new_object)

    def delete(self) -> None:
        """Delete Key-Value.

        .. versionadded:: v3.4

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.
        """
        path = self._key_value_path(self.id)
        self._client.delete(path)
