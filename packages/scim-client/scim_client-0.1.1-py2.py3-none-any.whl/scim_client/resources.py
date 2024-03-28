from typing import Dict, Any, Optional, List

from .defaults import Sentinel
from .utils import _to_dict_without_not_given, _to_snake_cased


class BaseResource:
    def to_dict(self):
        return _to_dict_without_not_given(self)

    def to_snake_cased_dict(self) -> Dict[str, Any]:
        return _to_snake_cased(_to_dict_without_not_given(self))


class UserMeta(BaseResource):
    resource_type: str = "User"
    created: str
    last_modified: str
    location: str

    def __init__(self, created: str, last_modified: str, location: str) -> None:
        self.created = created
        self.last_modified = last_modified
        self.location = location


class UserName(BaseResource):
    given_name: str
    family_name: str
    middle_name: Optional[str]
    name_prefix: Optional[str]
    name_suffix: Optional[str]
    phonetic_representation: Optional[str]
    formatted: Optional[str]

    def __init__(
        self,
        given_name: str,
        family_name: str,
        middle_name: str = Sentinel,
        name_prefix: str = Sentinel,
        name_suffix: str = Sentinel,
        phonetic_representation: str = Sentinel,
        formatted: str = Sentinel,
    ):
        self.given_name = given_name
        self.family_name = family_name
        self.middle_name = middle_name
        self.name_prefix = name_prefix
        self.name_suffix = name_suffix
        self.phonetic_representation = phonetic_representation
        self.formatted = formatted


class UserEmail(BaseResource):
    value: str
    primary: Optional[bool]

    def __init__(self, value: str, primary: bool = Sentinel):
        self.value = value
        self.primary = primary


class User(BaseResource):
    id: str
    external_id: str
    user_name: str
    display_name: str
    active: bool
    meta: Dict
    name: UserName
    emails: List[UserEmail]
    schemas: List[str]
    extra_fields: Dict[str, Any]

    def __init__(
        self,
        *,
        id: str,
        external_id: str,
        user_name: str,
        active: bool,
        name: Dict,
        display_name: str,
        emails: List[Dict[str, str | bool]],
        schemas: List[str],
        meta: Optional[Dict],
        **kwargs
    ) -> None:
        self.user_name = user_name
        self.id = id
        self.external_id = external_id
        self.active = active
        self.name = UserName(**name)
        self.emails = [UserEmail(**e) for e in emails]
        self.display_name = display_name
        self.meta = meta
        self.schemas = schemas
        self.extra_fields = kwargs


class UserSearch(BaseResource):
    resources: List[User]
    total_results: int
    items_per_page: int
    start_index: int
    schemas: List[str] = ["urn:ietf:params:scim:api:messages:2.0:ListResponse"]

    def __init__(
        self,
        resources: List[Dict[str, Any]],
        total_results: int,
        items_per_page: int,
        start_index: int,
    ):
        self.resources = [User(**r) for r in resources]
        self.total_results = total_results
        self.items_per_page = items_per_page
        self.start_index = start_index
