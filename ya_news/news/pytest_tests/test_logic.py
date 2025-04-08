from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.conftest import NEW_COMMENT, TEXT


def test_user_can_create_comment(
    author_client,
    author,
    detail_url,
    new
):
    Comment.objects.all().delete()
    comments_count = Comment.objects.count()
    response = author_client.post(detail_url, data=NEW_COMMENT)
    comment = Comment.objects.get()
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == comments_count + 1
    assert comment.text == NEW_COMMENT['text']
    assert comment.news == new
    assert comment.author == author


def test_anonymous_cant_create_comment(client, detail_url):
    comments_count = Comment.objects.count()
    client.post(detail_url, data=NEW_COMMENT)
    assert Comment.objects.count() == comments_count


def test_user_cant_use_bad_words(author_client, detail_url):
    comments_count = Comment.objects.count()
    bad_words_data = {'text': f'{TEXT}, {BAD_WORDS[0]}, {TEXT}'}
    response = author_client.post(detail_url, data=bad_words_data)
    assert Comment.objects.count() == comments_count
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )


def test_author_can_delete_comment(
    author_client,
    delete_comment_url,
    detail_url,
    comment
):
    comments_count = Comment.objects.count()
    response = author_client.delete(delete_comment_url)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == comments_count - 1


def test_user_cant_delete_another_comment(
    reader_client,
    delete_comment_url,
    comment
):
    comments_count = Comment.objects.count()
    response = reader_client.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count


def test_author_can_edit_comment(
    author_client,
    detail_url,
    edit_comment_url,
    comment
):
    response = author_client.post(edit_comment_url, data=NEW_COMMENT)
    assertRedirects(response, f'{detail_url}#comments')
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == NEW_COMMENT['text']
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_user_cant_edit_another_comment(
        reader_client,
        edit_comment_url,
        comment,
):
    response = reader_client.post(edit_comment_url, data=NEW_COMMENT)
    assert response.status_code == HTTPStatus.NOT_FOUND
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == comment.text
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news
