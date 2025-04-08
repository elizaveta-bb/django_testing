from http import HTTPStatus as HTTPs

from notes.tests.base_test import BaseTest


class TestRoutes(BaseTest):

    def test_pages_availability(self):

        urls = (
            (self.url_home, self.client, HTTPs.OK, self.ANONYMOUS),
            (self.url_login, self.client, HTTPs.OK, self.ANONYMOUS),
            (self.url_logout, self.client, HTTPs.OK, self.ANONYMOUS),
            (self.url_signup, self.client, HTTPs.OK, self.ANONYMOUS),
            (self.url_detail, self.author_client, HTTPs.OK, self.AUTHOR),
            (self.url_edit, self.author_client, HTTPs.OK, self.AUTHOR),
            (self.url_delete, self.author_client, HTTPs.OK, self.AUTHOR),
            (self.url_add, self.reader_client, HTTPs.OK, self.READER),
            (self.url_success, self.reader_client, HTTPs.OK, self.READER),
            (self.url_list, self.reader_client, HTTPs.OK, self.READER),
            (self.url_detail, self.reader_client, HTTPs.NOT_FOUND,
             self.READER),
            (self.url_edit, self.reader_client, HTTPs.NOT_FOUND, self.READER),
            (self.url_delete, self.reader_client, HTTPs.NOT_FOUND,
             self.READER),
        )
        for current_url, current_client, status, user in urls:
            with self.subTest(
                url=current_url,
                client=current_client,
                status=status,
                user=user
            ):
                self.assertEqual(
                    current_client.get(current_url).status_code, status
                )

    def test_redirects(self):

        urls = (
            self.url_add,
            self.url_success,
            self.url_detail,
            self.url_edit,
            self.url_delete,
            self.url_list,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.url_login}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
