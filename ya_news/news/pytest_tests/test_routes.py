from http import HTTPStatus as HTTPs

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

from .conftest import ADMIN_CLIENT, ANONYMOUS, AUTHOR_CLIENT


@pytest.mark.parametrize(
    'url, current_client, status', (
        (lf('home_url'), ANONYMOUS, HTTPs.OK),
        (lf('detail_url'), ANONYMOUS, HTTPs.OK),
        (lf('login_url'), ANONYMOUS, HTTPs.OK),
        (lf('logout_url'), ANONYMOUS, HTTPs.OK),
        (lf('signup_url'), ANONYMOUS, HTTPs.OK),
        (lf('delete_comment_url'), AUTHOR_CLIENT, HTTPs.OK),
        (lf('edit_comment_url'), AUTHOR_CLIENT, HTTPs.OK),
        (lf('delete_comment_url'), ADMIN_CLIENT, HTTPs.NOT_FOUND),
        (lf('edit_comment_url'), ADMIN_CLIENT, HTTPs.NOT_FOUND),
    )
)
def test_pages_availability_for_users(db, url, current_client, status,
                                      comment):
    response = current_client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'url', (
        lf('delete_comment_url'),
        lf('edit_comment_url'),
    )
)
def test_redirects(client, url, login_url):
    actual_url = url
    expected_url = f'{login_url}?next={actual_url}'
    response = client.get(actual_url)
    assertRedirects(response, expected_url)
