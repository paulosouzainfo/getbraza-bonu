from pydantic import BaseModel
from typing import Optional

class Person(BaseModel):
    account_number: str
    application_id: str
    certified_account: Optional[bool] = False
    static_qr_code_img: Optional[str] = None
    wallet_pubkey: Optional[str] = None
    pubkey: Optional[str] = False
