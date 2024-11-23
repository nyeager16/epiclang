from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta

class Language(models.Model):
    name = models.CharField(max_length=100)
    abb = models.CharField(max_length=2)
    def __str__(self):
        return self.name

class Word(models.Model):
    word_text = models.CharField(max_length=40, db_index=True)
    lang = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    tag = models.CharField(max_length=60, null=True, db_index=True)
    wtype = models.CharField(max_length=60, null=True, db_index=True)
    abb = models.CharField(max_length=40, null=True, db_index=True)
    root = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.word_text

class Channel(models.Model):
    channel_url = models.CharField(max_length=100)
    channel_name = models.CharField(max_length=100, default="NA", null=True)

class Video(models.Model):
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    auto_generated = models.BooleanField(default=True)

class UserVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    percentage = models.FloatField(default=0.0)

class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_history')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='watch_history')
    watched_at = models.DateTimeField(default=now)
    start = models.FloatField(default=0.0)
    end = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)


class WordInstance(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    start = models.CharField(max_length=10)
    end = models.CharField(max_length=10)
    def __str__(self):
        return self.word.word_text

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    comprehension_level_min = models.IntegerField(default=0)
    comprehension_level_max = models.IntegerField(default=100)
    queue_CI = models.IntegerField(default=100)

class Definition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    definition_text = models.TextField()

    def __str__(self):
        return f"{self.word.word_text} - {self.definition_text}"

class UserWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    needs_review = models.BooleanField(default=True)
    interval = models.FloatField(default=1.0)
    repetitions = models.IntegerField(default=0)
    ease_factor = models.FloatField(default=2.5)
    next_review = models.DateTimeField(default=now)

    def update_review_schedule(self, rating):
        """
        Update the next review date and interval based on the user's rating.
        Rating system: 0 = Again, 1 = Hard, 2 = Good, 3 = Easy
        """

        if rating == 0:  # Again
            self.repetitions = 0
            self.interval = 1
            self.ease_factor = max(1.3, self.ease_factor - 0.2)

        elif rating == 1:  # Hard
            self.interval = max(1, int(self.interval * 1.2))
            self.ease_factor = max(1.3, self.ease_factor - 0.15)

        elif rating == 2:  # Good
            self.repetitions += 1
            self.interval = int(self.interval * self.ease_factor)
            self.ease_factor = max(1.3, self.ease_factor)

        elif rating == 3:  # Easy
            self.repetitions += 1
            self.interval = int(self.interval * self.ease_factor * 1.5)
            self.ease_factor += 0.1

        # Schedule the next review
        self.next_review = timezone.now() + timedelta(days=self.interval)
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.word.word_text}"
