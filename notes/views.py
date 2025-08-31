from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .forms import NoteForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .helpers import handle_pin_notes

def home_page(request):
    return render(request, 'notes/home_page.html')


# ############################ Notes #########################

@login_required(login_url='users:login-user')
def notes_page(request):
    notes = models.Note.objects.filter(author=request.user).order_by("-is_pinned", "-rank")

    total_notes = len(notes)

    pinned_notes = notes.filter(is_pinned=True).count()

    favorite_notes = notes.filter(is_favorite=True).count()

    categories = models.Category.objects.filter(author=request.user)

    total_categories =len(categories)

    return render(request, 'notes/notes_page.html', {'notes': notes, "categories": categories, 'total_notes':total_notes,'pinned_notes':pinned_notes, "favorite_notes":favorite_notes,"total_categories": total_categories})


@login_required(login_url='users:login-user')
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.author = request.user
            new_note.save()
            messages.success(request, "Note added successfully!")
            return redirect('notes:notes_page')
    else:
        form = NoteForm(user = request.user)
    return render(request, 'notes/add_note.html', {'form': form})


@login_required(login_url='users:login-user')
def delete_note(request, note_id):
    note = get_object_or_404(models.Note, pk=note_id, author=request.user)
    if request.method == 'POST':
        note.delete()
        messages.warning(request, "Note deleted successfully!")
    return redirect('notes:notes_page')


@login_required(login_url='users:login-user')
def update_note(request, note_id):
    note = get_object_or_404(models.Note, pk=note_id, author=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully!")
            return redirect("notes:notes_page")
    else:
        form = NoteForm(instance=note, user = request.user)
    return render(request, 'notes/update_note.html', {'form': form})


@login_required(login_url='users:login-user')
def search_page(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '').strip()
        notes = models.Note.objects.filter(title__icontains=searched, author=request.user)
        return render(request, 'notes/search_page.html', {'searched': searched, 'notes': notes})
    else:
        return render(request, 'notes/search_page.html', {'searched': '', 'notes': []})

@login_required(login_url="users:login-user")
def pin_note(request,note_id):
    note = get_object_or_404(models.Note,pk=note_id,author=request.user)
    if request.method=="POST":
       return handle_pin_notes(request,'pin',note)

@login_required
def favorite_note(request,note_id):
    note = get_object_or_404(models.Note, pk=note_id, author = request.user)
    if request.method =='POST':
        return handle_pin_notes(request,'favorite',note)


@login_required(login_url='users:login-user')
def favorite_notes_page(request):
    notes = models.Note.objects.filter(author=request.user,is_favorite=True).order_by("-is_pinned", "-rank")
    categories = models.Category.objects.filter(author=request.user)
    return render(request, 'notes/favorite_notes.html', {'notes': notes, "categories": categories})

# ############################ Categories #########################

@login_required(login_url='users:login-user')
def category_page(request, category_id):
    category = get_object_or_404(models.Category, pk=category_id, author=request.user)
    notes = category.note_set.filter(author=request.user).order_by("-is_pinned" , "-rank")
    categories = models.Category.objects.filter(author=request.user)
    return render(request, 'categories/category_page.html', {
        'notes': notes,
        'category': category,
        'categories': categories
    })


@login_required(login_url='users:login-user')
def add_note_category(request, category_id):
    category = get_object_or_404(models.Category, pk=category_id, author=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.category = category
            new_note.author = request.user
            new_note.save()
            messages.success(request, "Note added to category successfully!")
            return redirect('notes:category-page', category_id=category_id)
    else:
        form = NoteForm()
    return render(request, 'categories/add_note_category.html', {'form': form, 'category': category})


@login_required(login_url='users:login-user')
def delete_note_category(request, note_id, category_id):
    note = get_object_or_404(models.Note, pk=note_id, author=request.user, category_id=category_id)
    if request.method == 'POST':
        note.delete()
        messages.warning(request, "Note deleted from category successfully!")
    return redirect('notes:category-page', category_id=category_id)


@login_required(login_url='users:login-user')
def update_note_category(request, note_id, category_id):
    note = get_object_or_404(models.Note, pk=note_id, author=request.user, category_id=category_id)
    category = get_object_or_404(models.Category, pk=category_id, author=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            updated_note = form.save(commit=False)
            updated_note.category = category
            updated_note.save()
            messages.success(request, "Note updated successfully!")
            return redirect('notes:category-page', category_id=category_id)
    else:
        form = NoteForm(instance=note)

    return render(request, 'categories/update_note_category.html', {'form': form})

@login_required(login_url="users:login-user")
def pin_category_note(request,note_id,category_id):
    note = get_object_or_404(models.Note, pk=note_id, author = request.user, category_id = category_id)
    
    if request.method=="POST":
        return handle_pin_notes(request,'pin',note,'notes:category-page', category_id=category_id)


@login_required
def favorite_category_note(request,note_id,category_id):
    note = get_object_or_404(models.Note, pk=note_id, author = request.user,category_id=category_id)
    if request.method =='POST':
        return handle_pin_notes(request,'favorite',note,"notes:category-page",category_id=category_id)

################################ Cateogries data #################
@login_required(login_url='users:login-user')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.author = request.user
            new_category.save()
            messages.success(request, "Category added successfully!")
            return redirect("notes:notes_page")
    else:
        form = CategoryForm()
    return render(request, 'categories/add_category.html', {'form': form})


@login_required(login_url='users:login-user')
def delete_category(request, category_id):
    category = get_object_or_404(models.Category, pk=category_id, author=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully!")
    return redirect("notes:notes_page")


@login_required(login_url='users:login-user')
def update_category(request, category_id):
    category = get_object_or_404(models.Category, pk=category_id, author=request.user)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('notes:notes_page')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/update_category.html', {'form': form})

################## Favorite page #####

@login_required(login_url="users:login-user")
def pin_note_on_page(request,note_id):
    note = get_object_or_404(models.Note,pk=note_id,author=request.user)
    if request.method=="POST":
       return handle_pin_notes(request,'pin',note,"notes:favorite-notes-page")


@login_required
def favorite_note_on_page(request,note_id):
    note = get_object_or_404(models.Note, pk=note_id, author = request.user)
    if request.method =='POST':
        return handle_pin_notes(request,'favorite',note, "notes:favorite-notes-page")