from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware


from app.database import engine, Base, get_db
from app import models, schemas, crud

Base.metadata.create_all(bind=engine)



app = FastAPI(title="Support CRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
def read_root():
    return {"message": "Support CRM API is running"}


@app.post("/api/tickets", response_model=schemas.TicketCreateOut)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    db_ticket = crud.create_ticket(db, ticket)
    return db_ticket


@app.get("/api/tickets", response_model=list[schemas.TicketListOut])
def list_tickets(
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_tickets(db, status=status, search=search)


@app.get("/api/tickets/{ticket_id}", response_model=schemas.TicketDetailOut)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    db_ticket = crud.get_ticket_by_ticket_id(db, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@app.put("/api/tickets/{ticket_id}")
def update_ticket_endpoint(
    ticket_id: str, update: schemas.TicketUpdate, db: Session = Depends(get_db)
):
    db_ticket = crud.update_ticket(db, ticket_id, update)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return {"success": True, "updated_at": db_ticket.updated_at}


