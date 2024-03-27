from typing import Any, IO, Optional

import os

import pandas as pd
import ethos as ethos
from ethos import ethos_client
import urllib3

from .ethos_client.models.governed_object_metadata_update_data import (
    GovernedObjectMetadataUpdateData,
)
from .ethos_client.models.resource_create_type import ResourceCreateType
from .ethos_client.models.list_datasource import ListDatasource
from .ethos_client.api.blobs import create_blob
from .ethos_client.api.datasources import get_datasources
from .ethos_client.api.governed_objects import (
    create_governed_object,
    get_governed_objects,
    update_governed_object,
    update_governed_object_metadata,
)
from .ethos_client.api.governed_types import get_governed_types
from .ethos_client.api.resources import create_resource
from .ethos_client.models.blob_create import BlobCreate
from .ethos_client.models.governed_object_create import GovernedObjectCreate
from .ethos_client.models.governed_object_data import GovernedObjectData
from .ethos_client.models.governed_object_metadata_update import (
    GovernedObjectMetadataUpdate,
)
from .ethos_client.models.governed_object_update import GovernedObjectUpdate
from .ethos_client.models.governed_object_update_data import GovernedObjectUpdateData
from .ethos_client.models.governed_type import GovernedType
from .ethos_client.models.list_governed_object import ListGovernedObject
from .ethos_client.models.list_governed_type import ListGovernedType
from .ethos_client.models.resource_blob_link_create import ResourceBlobLinkCreate
from .ethos_client.models.resource_create import ResourceCreate

__all__ = [
    "Config",
    "Model",
    "ModelVersion",
    "ModelVersionConfig",
    "ModelVersion",
    "Resource",
]


class ApiException(ValueError):
    pass


class ModelMissingError(ValueError):
    pass


class Config:
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        api_host: Optional[str] = None,
        namespace_id: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get("ETHOS_API_KEY")
        self.api_host = api_host or os.environ.get("ETHOS_API", "https://api.ethosai.com")
        self.namespace_id = namespace_id or os.environ.get("ETHOS_NAMESPACE")

    def validate(self):
        if not self.api_key:
            raise ValueError(
                "ETHOS_API_KEY must be set in the environment or passed to ethos.config.api_key"
            )
        if not self.namespace_id:
            raise ValueError(
                "ETHOS_NAMESPACE must be set in the environment or passed to ethos.config.namespace_id"
            )


class EthosObject:
    def __init__(self):
        self._loaded = False
        self._object = None
        self._config = ethos.config
        self._client_config = None

    @property
    def _client(self):
        self._config.validate()
        api_client = ethos_client.AuthenticatedClient(
            raise_on_unexpected_status=True,
            base_url=self._config.api_host,
            prefix="Bearer",
            token=self._config.api_key,
        )
        return api_client


class Model(EthosObject):
    def __init__(
        self,
        *,
        namespace_id: str,
        name: str,
        governed_type_name: str = "Models",
        force_create: bool = False,
    ):
        self.namespace_id = namespace_id
        self.name = name
        self.governed_type_name = governed_type_name
        self._force_create = force_create
        self.__model = None
        super().__init__()

    def __repr__(self):
        return f"<Model {self.name}>"

    @property
    def _model(self):
        if self.__model:
            return self.__model

        with self._client as api_client:
            # Find the governed type we want to use (by default, one called "Models").
            governed_types: ListGovernedType = get_governed_types.sync(
                client=api_client,
                namespace_id=self.namespace_id,
                name=self.governed_type_name,
            )
            default_type = governed_types.data[0] if governed_types.data else None
            if not default_type:
                raise ApiException(
                    f"Governed type named `{self.governed_type_name}` not found "
                    f"in namespace {self.namespace_id}."
                )

            models_data: ListGovernedObject = get_governed_objects.sync(
                client=api_client,
                namespace_id=self.namespace_id,
                governed_type_id=default_type.id,
                name=self.name,
            )

            if models_data.data:
                model = models_data.data[0]
            else:
                if self._force_create:
                    model_create = GovernedObjectCreate(
                        namespace_id=self.namespace_id,
                        governed_type_id=default_type.id,
                        data=GovernedObjectData.from_dict({"name": self.name}),
                    )
                    model = create_governed_object.sync(client=api_client, body=model_create)
                else:
                    raise ApiException(
                        f"Model name not found - must be registered in Ethos first "
                        "or pass force_create=True. Got name: {self.name}"
                    )
        self.__model = model
        return self.__model

    def new_version(self):
        return ModelVersion(_loaded_model=self._model)


class ModelVersionConfig:
    decision_threshold = None


class ModelVersion(EthosObject):
    def __init__(
        self,
        id: Optional[str] = None,
        _loaded_model: Optional[dict] = None,
    ):
        super().__init__()

        self.model = (
            _loaded_model.model_dump() if hasattr(_loaded_model, "model_dump") else _loaded_model
        )
        self._model_version_config = ModelVersionConfig()

        if id:
            self.id = id  # TODO: load if ID is provided, and set self.model.
            raise NotImplementedError
        else:
            self._create()

    def __repr__(self):
        return f"<ModelVersion {self.id}>"

    def _create(self):
        if not self.model:
            raise ModelMissingError("Model must be loaded before creating a model version.")

        with self._client as api_client:
            # TODO: pass through other data for custom fields.
            governed_object_update = GovernedObjectUpdate(
                data=GovernedObjectUpdateData.from_dict({})
            )
            model_version = update_governed_object.sync(
                client=api_client,
                governed_object_id=self.model.base_id,
                body=governed_object_update,
            )

        self.id = model_version.id
        self._model_version = model_version

    @property
    def config(self):
        return self._model_version_config

    def track_training_data(
        self,
        name: str,
        *,
        df: pd.DataFrame,
        id_column: str,
        target_column: str,
        version_tags: Optional[list] = None,
        tags: Optional[list] = None,
    ):
        Resource(related=self).track_dataset(
            name=name,
            version_tags=version_tags,
            tags=["train"] + (tags or []),
            df=df,
            id_column=id_column,
            target_column=target_column,
        )

    def track_inference_data(
        self,
        name: str,
        *,
        df: pd.DataFrame,
        id_column: str,
        actual_values_column: str,
        predict_column: Optional[str] = None,
        predict_proba_column: Optional[str] = None,
        version_tags: Optional[list] = None,
        tags: Optional[list] = None,
    ):
        Resource(related=self).track_dataset(
            name=name,
            df=df,
            version_tags=version_tags,
            tags=["inference"] + (tags or []),
            id_column=id_column,
            actual_values_column=actual_values_column,
            predict_column=predict_column,
            predict_proba_column=predict_proba_column,
        )

    def track_protected_data(
        self,
        name: str,
        *,
        df: pd.DataFrame,
        id_column: str,
        version_tags: Optional[list] = None,
        tags: Optional[list] = None,
    ):
        Resource(related=self).track_dataset(
            name=name,
            version_tags=version_tags,
            tags=["protected"] + (tags or []),
            df=df,
            id_column=id_column,
        )

    def track_dataset(
        self,
        name: str,
        *,
        df: pd.DataFrame,
        id_column: str,
        version_tags: Optional[list] = None,
        tags: Optional[list] = None,
    ):
        Resource(related=self).track_dataset(
            name=name,
            df=df,
            id_column=id_column,
            version_tags=version_tags,
            tags=tags or [],
        )

    def track_file(
        self,
        name: str,
        *,
        file: IO[Any],
        mimetype: str,
        version_tags: Optional[list] = None,
        tags: Optional[list] = None,
    ):
        Resource(related=self).track_file(
            name=name,
            file=file,
            mimetype=mimetype,
            version_tags=version_tags,
            tags=tags or [],
        )

    def finalize(self):
        with self._client as api_client:
            governed_object_metadata_update = GovernedObjectMetadataUpdate(
                GovernedObjectMetadataUpdateData.from_dict({"ethos:model:state": "finalized"}),
            )
            # Remove the :version suffix from the id.
            base_id = self._model_version.version_metadata.id.split(":")[0]

            update_governed_object_metadata.sync(
                client=api_client,
                governed_object_metadata_id=base_id,
                body=governed_object_metadata_update,
            )


class Resource(EthosObject):
    def __init__(self, *, related: Any, defer: bool = True):
        self._default_datasource = None
        self.related = related
        super().__init__()

    @property
    def default_datasource(self):
        if self._default_datasource:
            return self._default_datasource
        with self._client as api_client:
            datasources: ListDatasource = get_datasources.sync(
                client=api_client,
                namespace_id=self._config.namespace_id,
            )

            if len(datasources.data) == 1:
                self._default_datasource = datasources.data[0]
            else:
                raise NotImplementedError(
                    f"Multi-datasource support has not been implemented. "
                    f"Expected exactly one, got: {len(datasources.data)}"
                )
        return self._default_datasource

    def _upload_blob(self, *, signed_upload_url: str, content: bytes):
        http = urllib3.PoolManager()
        headers = {"Content-Type": "application/octet-stream"}
        response = http.request("PUT", signed_upload_url, body=content, headers=headers)

        if response.status not in (200, 201):
            raise ApiException(f"Failed to upload blob. Got status code: {response.status}")
        return response

    def track_file(
        self,
        name: str,
        *,
        file: IO[Any],
        mimetype: str,
        version_tags: Optional[list] = None,
        tags: Optional[list] = None,
    ):
        version_tags = version_tags or []
        tags = tags or []
        with self._client as api_client:
            try:
                # 1) Create blob:
                datasource = self.default_datasource
                blob_create = BlobCreate(
                    datasource_id=datasource.id,
                    filename=name,
                    mimetype=mimetype,
                )
                blob = create_blob.sync(client=api_client, body=blob_create)

                # 2) Upload the blob:
                self._upload_blob(
                    signed_upload_url=blob.signed_upload_url,  # type: ignore
                    content=file.read(),
                )

                # 3) Create the resource:
                resource_blob_link_creates = [ResourceBlobLinkCreate(blob_id=blob.id)]
                resource_create = ResourceCreate(
                    type=ResourceCreateType.FILE,
                    name=name,
                    related_id=self.related.id,
                    version_tags=version_tags,
                    tags=tags,
                    resource_blob_links=resource_blob_link_creates,
                )
                create_resource.sync(client=api_client, body=resource_create)
            except ApiException as e:
                print("Exception when calling API: %s\n" % e)

    def track_dataset(
        self,
        name: str,
        *,
        df: pd.DataFrame,
        version_tags: Optional[list] = None,
        tags: Optional[list] = None,
        id_column: Optional[str] = None,
        actual_values_column: Optional[str] = None,
        target_column: Optional[str] = None,
        predict_column: Optional[str] = None,
        predict_proba_column: Optional[str] = None,
    ):
        version_tags = version_tags or []
        tags = tags or []
        with self._client as api_client:
            try:
                # 1) Create blob:
                datasource = self.default_datasource
                blob_create = BlobCreate(
                    datasource_id=datasource.id,
                    filename=f"{name}.csv",
                    mimetype="text/csv",
                )
                blob = create_blob.sync(client=api_client, body=blob_create)

                # 2) Upload the CSV to the blob:
                self._upload_blob(
                    signed_upload_url=blob.signed_upload_url,  # type: ignore
                    content=df.to_csv(index=False).encode("utf-8"),
                )

                # 3) Create the dataset schema:
                column_creates = []
                if id_column:
                    column_create = {
                        "name": id_column,
                        "type": "id",
                        "dtype": df[id_column].dtype.name,
                    }
                    column_creates.append(column_create)
                if target_column:
                    column_create = {
                        "name": target_column,
                        "type": "target",
                        "dtype": df[target_column].dtype.name,
                    }
                    column_creates.append(column_create)
                if actual_values_column:
                    column_create = {
                        "name": actual_values_column,
                        "type": "actual_values",
                        "dtype": df[actual_values_column].dtype.name,
                    }
                    column_creates.append(column_create)
                if predict_column:
                    column_create = {
                        "name": predict_column,
                        "type": "predict",
                        "dtype": df[predict_column].dtype.name,
                    }
                    column_creates.append(column_create)
                if predict_proba_column:
                    column_create = {
                        "name": predict_proba_column,
                        "type": "predict_proba",
                        "dtype": df[predict_proba_column].dtype.name,
                    }
                    column_creates.append(column_create)
                if "protected" in tags:
                    for column in set(df.columns):
                        if column == id_column:
                            continue
                        column_create = {
                            "name": column,
                            "type": "protected",
                            "dtype": df[column].dtype.name,
                        }
                        column_creates.append(column_create)

                dataset_schema_create = {
                    "columns": column_creates,
                }

                # Add any columns that are not already in the schema.
                # TODO: we will likely remove this in preference for server-side detection later.
                column_create_names = [column["name"] for column in column_creates]
                for column in [
                    column for column in df.columns if column not in column_create_names
                ]:
                    column_create = {
                        "name": column,
                        "type": "default",
                        "dtype": df[column].dtype.name,
                    }
                    column_creates.append(column_create)

                # 4) Create the resource:
                resource_blob_link_creates = [ResourceBlobLinkCreate(blob_id=blob.id)]
                resource_create = ResourceCreate(
                    type=ResourceCreateType.DATASET,
                    name=name,
                    related_id=self.related.id,
                    version_tags=version_tags,
                    tags=tags,
                    resource_blob_links=resource_blob_link_creates,
                    dataset_schema=dataset_schema_create,  # type: ignore
                )
                create_resource.sync(client=api_client, body=resource_create)
            except ApiException as e:
                print("Exception when calling API: %s\n" % e)
