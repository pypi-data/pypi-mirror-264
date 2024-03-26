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

import contextlib
import json
import os
from typing import Any, Dict, Generator, List, Optional, Set, Tuple, Union

from requests_toolbelt import MultipartEncoder
import trafaret as t
from typing_extensions import TypedDict

from datarobot._compat import String
from datarobot.models.api_object import APIObject
from datarobot.models.runtime_parameters import RuntimeParameter, RuntimeParameterValue
from datarobot.utils import camelize
from datarobot.utils.pagination import unpaginate


class CustomJobFileItem(APIObject):
    """A file item attached to a DataRobot custom job.

    .. versionadded:: v3.4

    Attributes
    ----------
    id: str
        The ID of the file item.
    file_name: str
        The name of the file item.
    file_path: str
        The path of the file item.
    file_source: str
        The source of the file item.
    created_at: str
        ISO-8601 formatted timestamp of when the version was created.
    """

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("file_name"): String(),
            t.Key("file_path"): String(),
            t.Key("file_source"): String(),
            t.Key("created") >> "created_at": String(),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(
        self,
        id: str,
        file_name: str,
        file_path: str,
        file_source: str,
        created_at: str,
    ) -> None:
        self.id = id
        self.file_name = file_name
        self.file_path = file_path
        self.file_source = file_source
        self.created_at = created_at


class CustomJobFileItemType(TypedDict):
    id: str
    file_name: str
    file_path: str
    file_source: str
    created_at: str


class CustomJob(APIObject):
    """A DataRobot custom job.

    .. versionadded:: v3.4

    Attributes
    ----------
    id: str
        id of the custom job
    name: str
        name of the custom job
    created_at: str
        ISO-8601 formatted timestamp of when the version was created
    items: List[CustomJobFileItem]
        a list of file items attached to the custom job
    description: str, optional
        custom job description
    environment_id: str, optional
        id of the environment to use with the custom job
    environment_version_id: str, optional
        id of the environment version to use with the custom job
    """

    _path = "customJobs/"

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("name"): String(),
            t.Key("created") >> "created_at": String(),
            t.Key("items"): t.List(CustomJobFileItem.schema),
            t.Key("description", optional=True): t.Or(
                String(max_length=10000, allow_blank=True), t.Null()
            ),
            t.Key("environment_id", optional=True): t.Or(String(), t.Null()),
            t.Key("environment_version_id", optional=True): t.Or(String(), t.Null()),
            t.Key("entry_point", optional=True): t.Or(String(), t.Null()),
            t.Key("runtime_parameters", optional=True): t.List(RuntimeParameter.schema),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(
        self,
        id: str,
        name: str,
        created_at: str,
        items: List[CustomJobFileItemType],
        description: Optional[str] = None,
        environment_id: Optional[str] = None,
        environment_version_id: Optional[str] = None,
        entry_point: Optional[str] = None,
        runtime_parameters: Optional[List[RuntimeParameter]] = None,
    ) -> None:
        self.id = id
        self.description = description
        self.name = name
        self.created_at = created_at
        self.items = [CustomJobFileItem(**data) for data in items]

        self.environment_id = environment_id
        self.environment_version_id = environment_version_id
        self.entry_point = entry_point

        self.runtime_parameters = (
            [RuntimeParameter(**param) for param in runtime_parameters]  # type: ignore[arg-type]
            if runtime_parameters
            else None
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name or self.id!r})"

    def _update_values(self, new_response: CustomJob) -> None:
        fields: Set[str] = self._fields()  # type: ignore[no-untyped-call]
        for attr in fields:
            new_value = getattr(new_response, attr)
            setattr(self, attr, new_value)

    @classmethod
    def _custom_job_path(cls, custom_job_id: str) -> str:
        return f"{cls._path}{custom_job_id}/"

    @classmethod
    def create(
        cls,
        name: str,
        environment_id: Optional[str] = None,
        environment_version_id: Optional[str] = None,
        folder_path: Optional[str] = None,
        files: Optional[Union[List[Tuple[str, str]], List[str]]] = None,
        file_data: Optional[Dict[str, str]] = None,
        runtime_parameter_values: Optional[List[RuntimeParameterValue]] = None,
    ) -> CustomJob:
        """Create a custom job.

        .. versionadded:: v3.4

        Parameters
        ----------
        name: str
            The name of the custom job
        environment_id: Optional[str]
            The environment id to use for custom job runs.
            Must be specified in order to run the custom job.
        environment_version_id: Optional[str]
            The environment version id to use for custom job runs.
            If not specified, the latest version of the execution environment will be used.
        folder_path: Optional[str]
            The path to a folder containing files to be uploaded.
            Each file in the folder is uploaded under path relative
            to a folder path.
        files: Optional[Union[List[Tuple[str, str]], List[str]]]
            The files to be uploaded to the custom job.
            The files can be defined in 2 ways:
            1. List of tuples where 1st element is the local path of the file to be uploaded
            and the 2nd element is the file path in the custom job file system.
            2. List of local paths of the files to be uploaded.
            In this case files are added to the root of the custom model file system.
        file_data: Optional[Dict[str, str]]
            The files content to be uploaded to the custom job.
            Defined as a dictionary where keys are the file paths in the custom job file system
            and values are the files content.
        runtime_parameter_values: Optional[List[RuntimeParameterValue]]
            Additional parameters to be injected into a model at runtime. The fieldName
            must match a fieldName that is listed in the runtimeParameterDefinitions section
            of the model-metadata.yaml file.

        Returns
        -------
        CustomJob
            created custom job

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        upload_data: List[Tuple[str, Any]] = [
            ("name", name),
        ]

        if environment_id:
            upload_data.append(
                ("environmentId", environment_id),
            )
        if environment_version_id:
            upload_data.append(
                ("environmentVersionId", environment_version_id),
            )

        if runtime_parameter_values is not None:
            upload_data.append(
                (
                    "runtimeParameterValues",
                    json.dumps(
                        [
                            {camelize(k): v for k, v in param.to_dict().items()}
                            for param in runtime_parameter_values
                        ]
                    ),
                )
            )

        with cls._process_files_upload(folder_path, files, file_data) as file_upload_data:
            encoder = MultipartEncoder(fields=upload_data + file_upload_data)
            headers = {"Content-Type": encoder.content_type}
            response = cls._client.request("post", cls._path, data=encoder, headers=headers)

        return cls.from_server_data(response.json())

    @staticmethod
    def _verify_folder_path(folder_path: Optional[str]) -> None:
        if folder_path and not os.path.exists(folder_path):
            raise ValueError(f"The folder: {folder_path} does not exist.")

    @classmethod
    @contextlib.contextmanager
    def _process_files_upload(
        cls,
        folder_path: Optional[str] = None,
        files: Optional[Union[List[Tuple[str, str]], List[str]]] = None,
        file_data: Optional[Dict[str, str]] = None,
    ) -> Generator[List[Tuple[str, Any]], None, None]:
        """Process file-related argument and prepare them for the uploading."""
        upload_data: List[Tuple[str, Any]] = []

        cls._verify_folder_path(folder_path)

        with contextlib.ExitStack() as stack:
            if folder_path:
                for dir_name, _, file_names in os.walk(folder_path):
                    for file_name in file_names:
                        file_path = os.path.join(dir_name, file_name)
                        file = stack.enter_context(open(file_path, "rb"))

                        upload_data.append(("file", (os.path.basename(file_path), file)))
                        upload_data.append(("filePath", os.path.relpath(file_path, folder_path)))

            if files:
                # `paths` is a dict of (target file path, source file path) pairs, where
                # - target file path - is the file path on the custom job filesystem
                # - source file path - is the file path of the file to be uploaded
                paths: List[Tuple[str, str]]
                if isinstance(files[0], tuple):
                    paths = files  # type: ignore[assignment]
                else:
                    paths = []
                    for p in files:
                        source_file_path: str = p  # type: ignore[assignment]
                        paths.append((source_file_path, os.path.basename(source_file_path)))

                for source_file_path, target_file_path in paths:
                    source_file = stack.enter_context(open(source_file_path, "rb"))

                    upload_data.append(("file", (os.path.basename(target_file_path), source_file)))
                    upload_data.append(("filePath", target_file_path))

            if file_data:
                for target_file_path, content in file_data.items():
                    upload_data.append(("file", (os.path.basename(target_file_path), content)))
                    upload_data.append(("filePath", target_file_path))

            yield upload_data

    @classmethod
    def list(cls) -> List[CustomJob]:
        """List custom jobs.

        .. versionadded:: v3.4

        Returns
        -------
        List[CustomJob]
            a list of custom jobs

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        data = unpaginate(cls._path, None, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, custom_job_id: str) -> CustomJob:
        """Get custom job by id.

        .. versionadded:: v3.4

        Parameters
        ----------
        custom_job_id: str
            the id of the custom job

        Returns
        -------
        CustomJob
            retrieved custom job

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        path = cls._custom_job_path(custom_job_id)
        return cls.from_location(path)

    def update(
        self,
        name: Optional[str] = None,
        entry_point: Optional[str] = None,
        environment_id: Optional[str] = None,
        environment_version_id: Optional[str] = None,
        description: Optional[str] = None,
        folder_path: Optional[str] = None,
        files: Optional[Union[List[Tuple[str, str]], List[str]]] = None,
        file_data: Optional[Dict[str, str]] = None,
        runtime_parameter_values: Optional[List[RuntimeParameterValue]] = None,
    ) -> None:
        """Update custom job properties.

        .. versionadded:: v3.4

        Parameters
        ----------
        name: str
            The custom job name
        entry_point: Optional[str]
            The custom job file item id to use as an entry point of the custom job.
        environment_id: Optional[str]
            The environment id to use for custom job runs.
            Must be specified in order to run the custom job.
        environment_version_id: Optional[str]
            The environment version id to use for custom job runs.
            If not specified, the latest version of the execution environment will be used.
        description: str
            The custom job description
        folder_path: Optional[str]
            The path to a folder containing files to be uploaded.
            Each file in the folder is uploaded under path relative
            to a folder path.
        files: Optional[Union[List[Tuple[str, str]], List[str]]]
            The files to be uploaded to the custom job.
            The files can be defined in 2 ways:
            1. List of tuples where 1st element is the local path of the file to be uploaded
            and the 2nd element is the file path in the custom job file system.
            2. List of local paths of the files to be uploaded.
            In this case files are added to the root of the custom model file system.
        file_data: Optional[Dict[str, str]]
            The files content to be uploaded to the custom job.
            Defined as a dictionary where keys are the file paths in the custom job file system
            and values are the files content.
        runtime_parameter_values: Optional[List[RuntimeParameterValue]]
            Additional parameters to be injected into a model at runtime. The fieldName
            must match a fieldName that is listed in the runtimeParameterDefinitions section
            of the model-metadata.yaml file.

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        path = self._custom_job_path(self.id)

        upload_data: List[Tuple[str, Any]] = []

        if name:
            upload_data.append(("name", name))
        if entry_point:
            upload_data.append(("entryPoint", entry_point))
        if environment_id:
            upload_data.append(("environmentId", environment_id))
        if environment_version_id:
            upload_data.append(("environmentVersionId", environment_version_id))
        if description:
            upload_data.append(("description", description))
        if runtime_parameter_values:
            upload_data.append(
                (
                    "runtimeParameterValues",
                    json.dumps(
                        [
                            {camelize(k): v for k, v in param.to_dict().items()}
                            for param in runtime_parameter_values
                        ]
                    ),
                )
            )

        with self._process_files_upload(folder_path, files, file_data) as file_upload_data:
            encoder = MultipartEncoder(fields=upload_data + file_upload_data)
            headers = {"Content-Type": encoder.content_type}
            response = self._client.request("patch", path, data=encoder, headers=headers)

        data = response.json()
        new_version = CustomJob.from_server_data(data)
        self._update_values(new_version)

    def delete(self) -> None:
        """Delete custom job.

        .. versionadded:: v3.4

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.
        """
        url = f"{self._path}{self.id}/"
        self._client.delete(url)

    def refresh(self) -> None:
        """Update custom job with the latest data from server.

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
