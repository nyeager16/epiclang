import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from app.models import Language, Word, Video, UserVideoCI, WatchHistory, UserWord, Channel

@pytest.fixture
def language():
    """Fixture to create a language."""
    return Language.objects.create(name="Polish", abb="pl")

@pytest.fixture
def word(language):
    """Fixture to create a word."""
    return Word.objects.create(word_text="tak", lang=language)

@pytest.fixture
def video(language):
    """Fixture to create a video."""
    channel = Channel.objects.create(channelurl="http://example.com", channel_name="Example Channel", lastUpdated=timezone.now())
    return Video.objects.create(url="http://example.com/video1", title="Polish Video", channel=channel, language=language)

@pytest.fixture
def user():
    """Fixture to create a user."""
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def user_word(user, word):
    """Fixture to create a UserWord."""
    return UserWord.objects.create(user=user, word=word, needs_review=True)

@pytest.mark.django_db
def test_create_user_word(user, word):
    """Test that a UserWord instance is created correctly."""
    user_word = UserWord.objects.get(user=user, word=word)
    assert user_word.user.username == 'testuser'
    assert user_word.word.word_text == 'tak'
