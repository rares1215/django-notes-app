from django.contrib import messages
from django.shortcuts import redirect,render
from .forms import NoteForm


def handle_pin_notes(request,action,note,redirect_url = "notes:notes_page",category_id=None):
    if action =="pin":
        if not note.is_pinned:
            note.is_pinned = True
            note.rank =1
            note.save()
            messages.success(request,"Note Pinned!")
        else:
            note.is_pinned = False
            note.rank=0
            note.save()
            messages.info(request,"Note Unpinned!")
    elif action =='favorite':
        if not note.is_favorite:
            note.is_favorite = True
            note.save()
            messages.success(request,f'Added {note.title} to favorites')
        else:
            note.is_favorite = False
            note.save()
            messages.info(request,f'Remove {note.title} from favorites')
    if category_id:
        return redirect(redirect_url, category_id=category_id)
    return redirect(redirect_url)