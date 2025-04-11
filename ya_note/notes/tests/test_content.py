from notes.forms import NoteForm
from notes.tests.base_test import BaseTest


class TestContent(BaseTest):
    def test_notes_list_for_different_users(self):
        users_statuses = (
            (self.author_client, self.assertIn),
            (self.reader_client, self.assertNotIn),
        )
        for user, assert_method in users_statuses:
            with self.subTest(user=user):
                response = user.get(self.url_list)
                object_notes = response.context['object_list']
                assert_method(self.note, object_notes)

    def test_create_and_add_note_pages_contains_form(self):
        urls = (
            (self.url_add),
            (self.url_edit)
        )
        for url in urls:
            with self.subTest(name=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
