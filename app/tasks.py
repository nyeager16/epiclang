from background_task import background
from django.contrib.auth.models import User
from .models import Word, WordInstance, Definition, UserWord, UserVideo, Video, UserPreferences
from django.db.models import Q
from deep_translator import GoogleTranslator


# poetry run python manage.py process_tasks

@background()
def calculate_video_CI(user_id):
    user = User.objects.get(id=user_id)
    language = UserPreferences.objects.get(user=user).language
    videos = Video.objects.filter(language=language)

    # Get all root words connected to the user via UserWord
    user_root_words = UserWord.objects.filter(user=user).values_list('word_id', flat=True)

    # Get both root words and their conjugations (words whose root is one of the user's root words)
    user_known_words = Word.objects.filter(Q(id__in=user_root_words) | Q(root_id__in=user_root_words)).values_list('id', flat=True)

    for video in videos:
        word_instances = WordInstance.objects.filter(video=video)
        total_words = word_instances.count()
        learned_words = word_instances.filter(word_id__in=user_known_words).count()

        comprehension_percentage = (learned_words / total_words * 100) if total_words > 0 else 0
        comprehension_percentage = round(comprehension_percentage)

        user_video, created = UserVideo.objects.get_or_create(
            user=user, video=video,
            defaults={'percentage': comprehension_percentage}  # Only set if it's created
        )
        if not created:
            # If the record already existed, update the percentage
            user_video.percentage = comprehension_percentage
            user_video.save()
