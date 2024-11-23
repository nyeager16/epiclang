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

'''
def test_update_review_schedule(user_word):
    """Test that the review schedule updates correctly for a rating."""
    # Before update
    old_interval = user_word.interval
    user_word.update_review_schedule(rating=3)  # Easy

    assert user_word.interval > old_interval  # Interval should have increased
    assert user_word.next_review > timezone.now()  # Next review should be in the future


def test_user_video_comprehension(user, video):
    """Test that UserVideoCI is created or updated correctly."""
    user_video, created = UserVideoCI.objects.update_or_create(
        user=user, video=video, defaults={'percentage': 50.0}
    )
    assert user_video.percentage == 50.0
    assert created is True  # Ensure it was created

    # Update comprehension percentage
    user_video.percentage = 75.0
    user_video.save()
    user_video.refresh_from_db()  # Refresh to get the updated value
    assert user_video.percentage == 75.0


def test_watch_history_creation(user, video):
    """Test creating a WatchHistory entry for a user watching a video."""
    watch_history = WatchHistory.objects.create(
        user=user, video=video, watched_at=timezone.now(), progress=0.5, completed=False
    )
    assert watch_history.user.username == 'testuser'
    assert watch_history.video.title == 'Fruit Video'
    assert watch_history.progress == 0.5


def test_unique_watch_history(user, video):
    """Test the unique constraint on WatchHistory."""
    WatchHistory.objects.create(user=user, video=video, watched_at=timezone.now(), progress=0.5, completed=False)
    
    # Attempt to create a duplicate
    with pytest.raises(Exception):  # Expecting an integrity error (unique constraint violation)
        WatchHistory.objects.create(user=user, video=video, watched_at=timezone.now(), progress=1.0, completed=True)


def test_language_str(language):
    """Test the string representation of the Language model."""
    assert str(language) == "English"


def test_word_str(word):
    """Test the string representation of the Word model."""
    assert str(word) == "apple"


def test_channel_str(video):
    """Test the string representation of the Channel model."""
    assert str(video.channel) == "Example Channel"


def test_video_str(video):
    """Test the string representation of the Video model."""
    assert str(video) == "Fruit Video"


def test_word_instance_creation(word, video):
    """Test creating a WordInstance."""
    word_instance = WordInstance.objects.create(word=word, video=video, start="00:00", end="00:10")
    assert word_instance.word.word_text == "apple"
    assert word_instance.video.title == "Fruit Video"
    assert word_instance.start == "00:00"
    assert word_instance.end == "00:10"
'''