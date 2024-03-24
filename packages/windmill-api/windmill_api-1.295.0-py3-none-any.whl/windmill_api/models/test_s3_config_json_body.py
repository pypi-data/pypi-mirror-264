from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TestS3ConfigJsonBody")


@_attrs_define
class TestS3ConfigJsonBody:
    """
    Attributes:
        bucket (Union[Unset, str]):
        region (Union[Unset, str]):
        access_key (Union[Unset, str]):
        secret_key (Union[Unset, str]):
        endpoint (Union[Unset, str]):
    """

    bucket: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    access_key: Union[Unset, str] = UNSET
    secret_key: Union[Unset, str] = UNSET
    endpoint: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bucket = self.bucket
        region = self.region
        access_key = self.access_key
        secret_key = self.secret_key
        endpoint = self.endpoint

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if bucket is not UNSET:
            field_dict["bucket"] = bucket
        if region is not UNSET:
            field_dict["region"] = region
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
        bucket = d.pop("bucket", UNSET)

        region = d.pop("region", UNSET)

        access_key = d.pop("access_key", UNSET)

        secret_key = d.pop("secret_key", UNSET)

        endpoint = d.pop("endpoint", UNSET)

        test_s3_config_json_body = cls(
            bucket=bucket,
            region=region,
            access_key=access_key,
            secret_key=secret_key,
            endpoint=endpoint,
        )

        test_s3_config_json_body.additional_properties = d
        return test_s3_config_json_body

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
