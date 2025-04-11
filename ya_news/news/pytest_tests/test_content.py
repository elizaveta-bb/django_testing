import pytest

from news.forms import CommentForm
from .conftest import ANONYMOUS, AUTHOR_CLIENT, NEWS_COUNT


def test_news_count_order_and_count_on_homepage(
        client,
        home_url,
        bulk_news_creation
):

    response = client.get(home_url)
    news_items = list(response.context['object_list'])
    assert news_items == sorted(news_items, key=lambda x: x.date, reverse=True)
    assert len(news_items) == NEWS_COUNT


def test_comments_order_and_correct_form_type(
        client,
        detail_url,
        new,
        multiply_comments
):

    response = client.get(detail_url)
    new = response.context['news']
    all_comments = list(new.comment_set.all())
    assert 'news' in response.context
    assert all_comments == sorted(all_comments, key=lambda x: x.created)


@pytest.mark.parametrize(
    'current_client, status',
    ((ANONYMOUS, False), (AUTHOR_CLIENT, True)),
)
def test_form_in_context(current_client, detail_url, status):
    response = current_client.get(detail_url)
    form_in_context = 'form' in response.context
    assert form_in_context is status

@pytest.mark.parametrize(
    'current_client',
    (AUTHOR_CLIENT,),
)
def test_form_type_in_context(current_client, detail_url):
    response = current_client.get(detail_url)
    assert isinstance(response.context['form'], CommentForm)