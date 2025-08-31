from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from notes.models import Note


class NotesViewTest(TestCase):
    def setUp(self):
        # User creation and log in
        self.user = User.objects.create_user(username='test', password='12345')
        self.client.login(username='test', password='12345')

        # making a note for the user
        self.note = Note.objects.create(
            title='Test Note',
            content='Test Content',
            author=self.user
        )

    def test_notes_page_loads(self):
        """Loading the page corectly for the user"""
        response = self.client.get(reverse('notes:notes_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")

    def test_create_note(self):
        """User can add note"""
        response = self.client.post(reverse('notes:add-note'), {
            'title': 'New Note',
            'content': 'New Content'
        })
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Note.objects.count(), 2)

    def test_pin_note(self):
        """The pinned and unpinned functionality works"""
        url = reverse('notes:pin-note', args=[self.note.id])

        # Pinned
        response = self.client.post(url)
        self.note.refresh_from_db()
        self.assertTrue(self.note.is_pinned)
        self.assertEqual(response.status_code, 302)

        # Unpinned
        response = self.client.post(url)
        self.note.refresh_from_db()
        self.assertFalse(self.note.is_pinned)

    def test_favorite_note(self):
        """Note can be added and deleted from favorites"""
        url = reverse('notes:favorite-note', args=[self.note.id])

        # Favorite
        response = self.client.post(url)
        self.note.refresh_from_db()
        self.assertTrue(self.note.is_favorite)
        self.assertEqual(response.status_code, 302)

        # Unfavorite
        response = self.client.post(url)
        self.note.refresh_from_db()
        self.assertFalse(self.note.is_favorite)

    def test_redirect_if_not_logged_in(self):
        """If the user is not logged in it s redirected"""
        self.client.logout()
        response = self.client.get(reverse('notes:notes_page'))
        self.assertRedirects(response, '/users/login/?next=/notes-page/')

