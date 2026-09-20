from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# ---- Note schemas ----

class NoteCreate(BaseModel):
    note_text: str

class NoteOut(BaseModel):
    id: int
    note_text: str
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 (use orm_mode=True if on Pydantic v1)


# ---- Ticket schemas ----

class TicketCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None  # new note text to add, per the assignment's PUT spec

class TicketListOut(BaseModel):
    ticket_id: str
    customer_name: str
    subject: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class TicketDetailOut(BaseModel):
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    notes: List[NoteOut] = []

    class Config:
        from_attributes = True

class TicketCreateOut(BaseModel):
    ticket_id: str
    created_at: datetime