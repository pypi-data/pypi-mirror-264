from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestObjectStorageConfigJsonBody")


@_attrs_define
class TestObjectStorageConfigJsonBody:
    """
    Attributes:
        type (Union[Unset, str]):
        bucket (Union[Unset, str]):
        region (Union[Unset, str]):
        access_key (Union[Unset, str]):
        account_name (Union[Unset, str]):
        tenant_id (Union[Unset, str]):
        client_id (Union[Unset, str]):
        access_key (Union[Unset, str]):
        secret_key (Union[Unset, str]):
        endpoint (Union[Unset, str]):
    """

    type: Union[Unset, str] = UNSET
    bucket: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    access_key: Union[Unset, str] = UNSET
    account_name: Union[Unset, str] = UNSET
    tenant_id: Union[Unset, str] = UNSET
    client_id: Union[Unset, str] = UNSET
    access_key: Union[Unset, str] = UNSET
    secret_key: Union[Unset, str] = UNSET
    endpoint: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        bucket = self.bucket
        region = self.region
        access_key = self.access_key
        account_name = self.account_name
        tenant_id = self.tenant_id
        client_id = self.client_id
        access_key = self.access_key
        secret_key = self.secret_key
        endpoint = self.endpoint

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if bucket is not UNSET:
            field_dict["bucket"] = bucket
        if region is not UNSET:
            field_dict["region"] = region
        if access_key is not UNSET:
            field_dict["accessKey"] = access_key
        if account_name is not UNSET:
            field_dict["accountName"] = account_name
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if client_id is not UNSET:
            field_dict["clientId"] = client_id
        if access_key is not UNSET:
            field_dict["access_key"] = access_key
        if secret_key is not UNSET:
            field_dict["secret_key"] = secret_key
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        bucket = d.pop("bucket", UNSET)

        region = d.pop("region", UNSET)

        access_key = d.pop("accessKey", UNSET)

        account_name = d.pop("accountName", UNSET)

        tenant_id = d.pop("tenantId", UNSET)

        client_id = d.pop("clientId", UNSET)

        access_key = d.pop("access_key", UNSET)

        secret_key = d.pop("secret_key", UNSET)

        endpoint = d.pop("endpoint", UNSET)

        test_object_storage_config_json_body = cls(
            type=type,
            bucket=bucket,
            region=region,
            access_key=access_key,
            account_name=account_name,
            tenant_id=tenant_id,
            client_id=client_id,
            access_key=access_key,
            secret_key=secret_key,
            endpoint=endpoint,
        )

        test_object_storage_config_json_body.additional_properties = d
        return test_object_storage_config_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
