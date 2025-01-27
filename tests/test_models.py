import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from app.models import (
    Language, Word, Channel, Video, UserVideo, WatchHistory, WordInstance,
    UserPreferences, Definition, UserWord, Review
)
from datetime import timedelta

@pytest.fixture
def language():
    """Fixture to create a language."""
    return Language.objects.create(name="Polish", abb="pl")

@pytest.fixture
def user():
    """Fixture to create a user."""
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def word(language):
    """Fixture to create a word."""
    return Word.objects.create(word_text="tak", lang=language)

@pytest.fixture
def channel():
    """Fixture to create a channel."""
    return Channel.objects.create(channel_url="http://youtube.com/@test", channel_name="Example Channel")

@pytest.fixture
def video(language):
    """Fixture to create a video."""
    return Video.objects.create(url="http://youtube.com/video1", title="Polish Video", channel=channel, language=language)

@pytest.fixture
def user_word(user, word):
    """Fixture to create a UserWord."""
    return UserWord.objects.create(user=user, word=word)

@pytest.fixture
def word_instance(word, video):
    """Fixture to create a word instance."""
    return WordInstance.objects.create(word=word, video=video, start="0.1", end="10.2")

@pytest.mark.django_db
def test_language_creation(language):
    assert Language.objects.count() == 1
    assert str(language) == "Polish"

@pytest.mark.django_db
def test_create_user_word(user, word):
    """Test that a UserWord instance is created correctly."""
    user_word = UserWord.objects.get(user=user, word=word)
    assert user_word.user.username == 'testuser'
    assert user_word.word.word_text == 'tak'
