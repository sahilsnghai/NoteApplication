from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import database.models as models, schemas, auth
from auth import get_db

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

@router.post("/", response_model=schemas.NoteOut)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    db_note = models.Note(
        title=note.title,
        content=note.content,
        user_id=user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/", response_model=List[schemas.NoteOut])
def get_notes(db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    return db.query(models.Note).filter(models.Note.user_id == user.id).all()

@router.get("/{note_id}", response_model=schemas.NoteOut)
def get_note(note_id: str, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.user_id == user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(note_id: str, note: schemas.NoteCreate, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.user_id == user.id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str, db: Session = Depends(get_db), user=Depends(auth.get_current_user)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.user_id == user.id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()