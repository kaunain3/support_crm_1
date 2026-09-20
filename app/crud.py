import uuid
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas


def generate_ticket_id(db: Session) -> str:
    """Generate a sequential ticket ID like TKT-001, TKT-002, ..."""
    count = db.query(models.Ticket).count()
    return f"TKT-{count + 1:03d}"


def create_ticket(db: Session, ticket: schemas.TicketCreate) -> models.Ticket:
    db_ticket = models.Ticket(
        ticket_id=generate_ticket_id(db),
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        subject=ticket.subject,
        description=ticket.description,
        status="Open",
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)  # reload it so we get the DB-generated id/timestamps
    return db_ticket


def get_tickets(db: Session, status: str | None = None, search: str | None = None):
    query = db.query(models.Ticket)

    if status:
        query = query.filter(models.Ticket.status == status)

    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Ticket.customer_name.ilike(like_pattern),
                models.Ticket.customer_email.ilike(like_pattern),
                models.Ticket.ticket_id.ilike(like_pattern),
                models.Ticket.description.ilike(like_pattern),
            )
        )

    return query.order_by(models.Ticket.created_at.desc()).all()


def get_ticket_by_ticket_id(db: Session, ticket_id: str) -> models.Ticket | None:
    return db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()


def update_ticket(db: Session, ticket_id: str, update: schemas.TicketUpdate) -> models.Ticket | None:
    db_ticket = get_ticket_by_ticket_id(db, ticket_id)
    if not db_ticket:
        return None

    if update.status:
        db_ticket.status = update.status

    if update.notes:
        db_note = models.Note(ticket_id=db_ticket.id, note_text=update.notes)
        db.add(db_note)

    db.commit()
    db.refresh(db_ticket)
    return db_ticket