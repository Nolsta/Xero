from pydantic import BaseModel
from pydantic.class_validators import Optional


class Invoices(BaseModel):
    Type: str
    Contact: dict
    LineAmountTypes: str
    LineItems: list


class Invoice(BaseModel):
    Type: str
    Contact: dict
    LineAmountTypes: str
    LineItems: list
    InvoiceID: str


class Tokens(BaseModel):
    id_token: str
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: str
    scope: str


class Organisation(BaseModel):
    client_id: str
    # service_configuration: dict


class Ringier(BaseModel):
    username: str
    password: str


class CCube(BaseModel):
    event: Optional[str] = None
    venture_config_id: Optional[str] = None
    venture_reference: Optional[str] = None
    created_at: Optional[str] = None
    culture: Optional[str] = None
    action_type: Optional[str] = None
    action_reference: Optional[str] = None
    version: Optional[str] = None
    route: Optional[str] = None
    payload: dict
    service_configurations: dict
