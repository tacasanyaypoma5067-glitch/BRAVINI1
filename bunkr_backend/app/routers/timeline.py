# Timeline Router - Diary and Memory Lane
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional
from datetime import datetime, date

from app.database import get_db
from app.models import User, Note, File, Tag
from app.schemas import (
    NoteCreate,
    NoteResponse,
    TimelineResponse,
    TimelineEntry,
    OnThisDayResponse,
    MessageResponse,
)
from app.routers.auth import get_current_user

router = APIRouter(prefix="/timeline", tags=["Timeline"])


@router.post("/note", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new diary entry/note in the timeline.
    
    Optionally attach a media file (photo) to the note.
    """
    # Validate media file if provided
    has_media = False
    if note_data.media_file_id:
        media_file = db.query(File).filter(
            File.id == note_data.media_file_id,
            File.user_id == current_user.id
        ).first()
        
        if not media_file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Media file not found"
            )
        
        has_media = True
    
    # Create note
    new_note = Note(
        content=note_data.content,
        user_id=current_user.id,
        media_file_id=note_data.media_file_id,
        has_media=has_media
    )
    
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    
    return new_note


@router.get("/", response_model=TimelineResponse)
async def get_timeline(
    skip: int = 0,
    limit: int = 30,
    include_files: bool = True,
    tag_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get combined timeline of notes and files.
    
    Returns a unified chronological feed of diary entries and photos.
    """
    # Get notes
    notes_query = db.query(Note).filter(Note.user_id == current_user.id)
    
    if tag_id:
        # Filter notes by tag through associated media files
        notes_query = notes_query.join(File, isouter=True).join(Tag, isouter=True).filter(Tag.id == tag_id)
    
    notes = notes_query.order_by(Note.created_at.desc()).all()
    
    # Build timeline entries from notes
    entries = []
    
    for note in notes:
        tag_names = []
        if note.media_file and note.media_file.tags:
            tag_names = [tag.name for tag in note.media_file.tags]
        
        entry = TimelineEntry(
            id=note.id,
            type="note",
            content=note.content,
            created_at=note.created_at,
            tags=tag_names
        )
        entries.append(entry)
    
    # Get standalone files (not attached to notes) if requested
    if include_files:
        files_query = db.query(File).filter(
            File.user_id == current_user.id,
            File.id.notin_(db.query(Note.media_file_id).filter(Note.media_file_id != None))
        )
        
        if tag_id:
            files_query = files_query.join(File.tags).filter(Tag.id == tag_id)
        
        files = files_query.order_by(File.created_at.desc()).all()
        
        for file_obj in files:
            tag_names = [tag.name for tag in file_obj.tags] if file_obj.tags else []
            
            thumbnail_url = None
            if file_obj.file_type.startswith("image/"):
                thumbnail_url = f"/files/{file_obj.id}/thumbnail"
            
            entry = TimelineEntry(
                id=file_obj.id,
                type="file",
                filename=file_obj.original_filename,
                file_type=file_obj.file_type,
                thumbnail_url=thumbnail_url,
                created_at=file_obj.created_at,
                tags=tag_names
            )
            entries.append(entry)
    
    # Sort all entries by created_at descending
    entries.sort(key=lambda x: x.created_at, reverse=True)
    
    # Apply pagination
    total = len(entries)
    paginated_entries = entries[skip:skip + limit]
    
    return TimelineResponse(
        entries=paginated_entries,
        total=total,
        has_more=skip + limit < total
    )


@router.get("/on-this-day", response_model=OnThisDayResponse)
async def get_on_this_day(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get "Un Día Como Hoy" (On This Day) entries.
    
    Returns notes and files from previous years on the same month/day.
    """
    today = date.today()
    current_month = today.month
    current_day = today.day
    current_date_str = f"{current_month:02d}-{current_day:02d}"
    
    # Get notes from this day in previous years
    notes_query = db.query(Note).filter(
        Note.user_id == current_user.id,
        extract('month', Note.created_at) == current_month,
        extract('day', Note.created_at) == current_day,
        extract('year', Note.created_at) != today.year
    ).order_by(Note.created_at.desc())
    
    notes = notes_query.all()
    
    # Get files from this day in previous years (standalone or with notes)
    files_query = db.query(File).filter(
        File.user_id == current_user.id,
        extract('month', File.created_at) == current_month,
        extract('day', File.created_at) == current_day,
        extract('year', File.created_at) != today.year
    ).order_by(File.created_at.desc())
    
    files = files_query.all()
    
    # Build entries
    entries = []
    years_ago = []
    
    for note in notes:
        years = today.year - note.created_at.year
        years_ago.append(years)
        
        tag_names = []
        if note.media_file and note.media_file.tags:
            tag_names = [tag.name for tag in note.media_file.tags]
        
        entry = TimelineEntry(
            id=note.id,
            type="note",
            content=note.content,
            created_at=note.created_at,
            tags=tag_names
        )
        entries.append(entry)
    
    for file_obj in files:
        years = today.year - file_obj.created_at.year
        years_ago.append(years)
        
        tag_names = [tag.name for tag in file_obj.tags] if file_obj.tags else []
        
        thumbnail_url = None
        if file_obj.file_type.startswith("image/"):
            thumbnail_url = f"/files/{file_obj.id}/thumbnail"
        
        entry = TimelineEntry(
            id=file_obj.id,
            type="file",
            filename=file_obj.original_filename,
            file_type=file_obj.file_type,
            thumbnail_url=thumbnail_url,
            created_at=file_obj.created_at,
            tags=tag_names
        )
        entries.append(entry)
    
    # Sort by date (most recent first)
    entries.sort(key=lambda x: x.created_at, reverse=True)
    years_ago.sort(reverse=True)
    
    return OnThisDayResponse(
        current_date=current_date_str,
        entries=entries,
        years_ago=list(set(years_ago))  # Unique years
    )


@router.get("/note/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific note by ID."""
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return note


@router.put("/note/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    content: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing note."""
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    note.content = content
    note.updated_at = func.now()
    
    db.commit()
    db.refresh(note)
    
    return note


@router.delete("/note/{note_id}", response_model=MessageResponse)
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a note from the timeline."""
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    db.delete(note)
    db.commit()
    
    return {"message": "Note deleted successfully"}
