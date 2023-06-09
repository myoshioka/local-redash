from enum import Enum, IntEnum

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str
    auth_type: str
    email: str
    groups: list[int]
    is_disabled: bool
    is_email_verified: bool
    is_invitation_pending: bool
    profile_image_url: str
    created_at: str
    active_at: str
    updated_at: str
    disabled_at: str | None


class Query(BaseModel):
    id: int
    name: str
    description: str | None
    api_key: str
    is_archived: bool
    is_draft: bool
    is_favorite: bool
    is_safe: bool
    data_source_id: int
    last_modified_by_id: int
    latest_query_data_id: int | None
    options: dict
    query: str
    query_hash: str
    runtime: float | None
    schedule: str | None
    tags: list[str]
    version: int
    user: User
    retrieved_at: str | None
    updated_at: str
    created_at: str


class QueryList(BaseModel):
    __root__: list[Query]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def dict(self, **kwargs):
        return super().dict(**kwargs)['__root__']


class ResponseQuery(BaseModel):
    count: int
    page: int
    page_size: int
    results: list[Query]


class DataSourceType(Enum):
    POSTGRESQL = 'pg'
    MYSQL = 'mysql'
    BIGQUERY = 'bigquery'
    PYTHON = 'python'
    ATHENA = 'athena'


class DataSource(BaseModel):
    id: int
    name: str
    pause_reason: str | None
    syntax: str
    paused: int
    view_only: bool
    type: DataSourceType

    class Config:
        use_enum_values = True


class DataSourceDetail(BaseModel):
    id: int
    name: str
    scheduled_queue_name: str
    pause_reason: str | None
    queue_name: str
    syntax: str
    paused: int
    type: DataSourceType
    groups: dict[str, str | int | bool]
    options: dict[str, str | int | bool]

    class Config:
        use_enum_values = True


class DataSourceList(BaseModel):
    __root__: list[DataSource]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def dict(self, **kwargs):
        return super().dict(**kwargs)['__root__']


class LastModified(BaseModel):
    id: int
    name: str
    email: str
    auth_type: str
    is_disabled: bool
    profile_image_url: str
    is_invitation_pending: bool
    groups: list[int]
    is_email_verified: bool
    created_at: str
    active_at: str
    updated_at: str
    disabled_at: str | None


class Visualization(BaseModel):
    id: int
    name: str
    description: str
    type: str
    options: dict
    created_at: str
    updated_at: str


class QueryUpdate(BaseModel):
    id: int
    name: str
    api_key: str
    schedule: str | None
    description: str | None
    tags: list[str]
    options: dict
    is_safe: bool
    is_favorite: bool
    is_archived: bool
    is_draft: bool
    version: int
    query: str
    query_hash: str
    data_source_id: int
    latest_query_data_id: int | None
    user: User
    last_modified_by: LastModified
    visualizations: list[Visualization]
    created_at: str
    updated_at: str


class QueryResulColumn(BaseModel):
    friendly_name: str
    type: str | None
    name: str


class QueryResulRows(BaseModel):
    __root__: list[dict[str, str | int | float | bool | None]]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def dict(self, **kwargs):
        return super().dict(**kwargs)['__root__']


class QueryResultData(BaseModel):
    rows: QueryResulRows
    columns: list[QueryResulColumn]


class QueryResult(BaseModel):
    id: int
    data_source_id: int
    query_hash: str
    query: str
    runtime: float
    data: QueryResultData
    retrieved_at: str


class JobResultStatus(IntEnum):
    QUEUED = 1
    STARTED = 2
    FINISHED = 3
    FAILED = 4


class JobResult(BaseModel):
    id: str
    status: JobResultStatus
    query_result_id: int | None
    error: str
    updated_at: int

    class Config:
        use_enum_values = True


class SqlFormatDialects():

    DATASOURCE_DIALECTS_MMAPPING = {
        DataSourceType.ATHENA: 'athena',
        DataSourceType.BIGQUERY: 'bigquery',
        DataSourceType.MYSQL: 'mysql',
        DataSourceType.POSTGRESQL: 'postgres'
    }

    @classmethod
    def from_datasource_type(cls, source_type: DataSourceType) -> str:

        if source_type in cls.DATASOURCE_DIALECTS_MMAPPING:
            return cls.DATASOURCE_DIALECTS_MMAPPING[source_type]
        else:
            return 'ansi'
