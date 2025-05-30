import datetime

import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from pytest_lazyfixture import lazy_fixture

from news.models import Comment, News

ADMIN_CLIENT = lazy_fixture('admin_client')
AUTHOR_CLIENT = lazy_fixture('author_client')
ANONYMOUS = lazy_fixture('client')

TITLE = 'Заголовок'
TEXT = 'Текст'
COUNT_ADD = 1
COMMENTS_COUNT = 3
NEW_COMMENT = {'text': 'Новый текст'}
NEWS_COUNT = 10


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(
        username='Марти Макфлай',
        password='delorean'
    )


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(
        username='Морти Смит',
        password='Wubbalubbadubdub'
    )


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    yield client


@pytest.fixture
def news():
    return News.objects.create(
        title=TITLE,
        text=TEXT,
    )


@pytest.fixture
def bulk_news_creation():
    return News.objects.bulk_create(
        News(
            title=f'{TITLE} {i}',
            text=TEXT,
            date=datetime.datetime.now() + datetime.timedelta(minutes=i)
        ) for i in range(NEWS_COUNT)
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        author=author,
        news=news,
        text=TEXT
    )


@pytest.fixture
def multiply_comments(author, news):
    for index in range(COMMENTS_COUNT):
        comment = Comment.objects.create(
            author=author,
            news=news,
            text=f'{TEXT} {index}',
        )
        comment.created = timezone.now() + datetime.timedelta(days=index)
        comment.save()


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_comment_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')
