from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.base_test import BaseTest


class TestNoteCreation(BaseTest):
    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(
            self.url_add, data=self.form_data
        )
        self.assertRedirects(response, self.url_success)
        new_notes_count = Note.objects.count()
        self.assertEqual(new_notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_anonymous_cant_create_note(self):
        initial_notes_count = Note.objects.count()
        response = self.client.post(
            self.url_add, self.form_data
        )
        expected_url = f'{self.url_login}?next={self.url_add}'
        self.assertRedirects(response, expected_url)
        new_notes_count = Note.objects.count()
        self.assertEqual(new_notes_count, initial_notes_count)

    def test_unique_slug(self):
        note_count = Note.objects.count()
        self.form_data['slug'] = self.SLUG
        response = self.author_client.post(
            self.url_add, data=self.form_data)
        self.assertEqual(Note.objects.count(), note_count)
        self.assertFormError(
            response, 'form', 'slug', errors=f'{self.SLUG}{WARNING}'
        )

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('slug', None)
        response = self.author_client.post(self.url_add, data=self.form_data)
        self.assertRedirects(response, self.url_success)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        max_slug_length = Note._meta.get_field('slug').max_length
        expected_slug = slugify(self.form_data['title'])[:max_slug_length]
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            self.url_edit, data=self.form_data
        )
        self.assertRedirects(response, self.url_success)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.text, self.form_data['text'])
        self.assertEqual(updated_note.title, self.form_data['title'])
        self.assertEqual(updated_note.slug, self.form_data['slug'])
        self.assertEqual(updated_note.author, self.note.author)

    def test_author_can_delete_note(self):
        note_id = self.note.id
        response = self.author_client.post(self.url_delete)
        self.assertRedirects(response, self.url_success)
        self.assertFalse(
            Note.objects.filter(id=note_id).exists(),
            "Заметка не была удалена из базы данных"
        )

    def test_not_author_cant_edit_note(self):
        response = self.reader_client.post(
            self.url_edit,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(self.note.text, self.note.text)
        self.assertEqual(self.note.title, self.note.title)
        self.assertEqual(self.note.slug, self.note.slug)
        self.assertEqual(self.note.author, self.note.author)

    def test_not_author_cant_delete_note(self):
        initial_count = Note.objects.count()
        response = self.reader_client.post(self.url_delete)
        self.assertEqual(
            response.status_code,
            HTTPStatus.FORBIDDEN,
            "Проверьте, что не-автор не может удалить заметку"
        )
        self.assertEqual(
            Note.objects.count(),
            initial_count,
            "Проверьте, что количество заметок не изменилось"
        )
        self.assertTrue(
            Note.objects.filter(id=self.note.id).exists(),
            "Проверьте, что заметка не была удалена из базы данных"
        )
