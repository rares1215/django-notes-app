from django.urls import path
from . import views

app_name = 'notes'


urlpatterns = [
    ################## Notes urls##############################

    path('', views.home_page,name='home-page'),
    path('notes-page/', views.notes_page, name='notes_page'),
    path('add-note/', views.add_note, name='add-note'),
    path('delete-note/<note_id>',views.delete_note,name='delete-note'),
    path('update-note/<note_id>',views.update_note,name='update-note'),
    path('search-page/', views.search_page, name = 'search-page'),
    path('pin-note/<note_id>', views.pin_note,name='pin-note'),
    path('favorite-note/<note_id>', views.favorite_note,name='favorite-note'),
    path('favorite-notes-page', views.favorite_notes_page, name="favorite-notes-page"),

    ############ Cateogries urls#######################

    path('category-page/<category_id>', views.category_page,name='category-page'),

    path('add-note-category/<category_id>', views.add_note_category, name='add-note-category'),

    path('delete-note-category/<note_id>/<category_id>',views.delete_note_category,name='delete-note-category'),

    path('update-note-category/<note_id>/<category_id>',views.update_note_category,name='update-note-category'),

    path('add-category', views.add_category, name='add-category'),

    path('delete-category/<category_id>', views.delete_category,name='delete-category'),

    path('update-category/<category_id>', views.update_category,name='update-category'),

    path('pin-category-note/<note_id>/<category_id>', views.pin_category_note,name='pin-category-note'),

    path('favorite-category-note/<note_id>/<category_id>', views.favorite_category_note,name='favorite-category-note'),

    #### Favorite notes page########
    path('pin-note_on_page/<note_id>', views.pin_note_on_page,name='pin-note-on-page'),
    path('favorite-note-on-page/<note_id>', views.favorite_note_on_page,name='favorite-note-on-page'),

]
