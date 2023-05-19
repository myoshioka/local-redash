from pydantic import BaseModel, Field


class User(BaseModel):
    active_at: str
    auth_type: str
    created_at: str
    disabled_at: str | None
    email: str
    groups: list[int]
    id: int
    is_disabled: bool
    is_email_verified: bool
    is_invitation_pending: bool
    name: str
    profile_image_url: str
    updated_at: str


class Query(BaseModel):
    id: int
    name: str
    api_key: str
    created_at: str
    data_source_id: int
    description: str
    is_archived: bool
    is_draft: bool
    is_favorite: bool
    is_safe: bool
    last_modified_by_id: int
    latest_query_data_id: int
    options: dict
    query: str
    query_hash: str
    retrieved_at: str
    runtime: float
    schedule: str | None
    tags: list[str]
    updated_at: str
    version: int
    user: User


class ResponseQuery(BaseModel):
    count: int
    page: int
    page_size: int
    results: list[Query]
