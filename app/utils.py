from .models import Language, WordInstance, UserWord, UserVideo, Video, UserPreferences
from django.db.models.functions import Coalesce

def setup_user(user):
    videos = Video.objects.all()
    user_videos_to_create = [UserVideo(user=user,video=video) for video in videos]
    UserVideo.objects.bulk_create(user_videos_to_create)
    language = Language.objects.get(abb="pl")
    UserPreferences(user=user, language=language).save()


def get_video_data(videos, user=None, comprehension_level_min=0, comprehension_level_max=100):
    video_data = []
    for video in videos:
        if user:
            comprehension_percentage = UserVideo.objects.get(user=user, video=video).percentage
            if not (comprehension_level_min <= comprehension_percentage <= comprehension_level_max):
                continue
        else:
            comprehension_percentage = 0

        video_data.append({
            'pk': video.pk,
            'title': video.title,
            'url': video.url,
            'comprehension_percentage': comprehension_percentage,
        })
    return video_data

def get_CI_video_sections(user, percentage, count):
    known_words = UserWord.objects.filter(user=user).values_list('word', flat=True)
    known_words = set(known_words)
    preferences = UserPreferences.objects.get(user=user)
    videos = Video.objects.filter(language=preferences.language).exclude(
        watch_history__user=user
    )

    sections = []

    for video in videos:
        video_words = (
            WordInstance.objects
            .filter(video=video)
            .annotate(
                root_word=Coalesce('word__root', 'word')
            )
            .values('root_word', 'start', 'end')
        )

        video_sections = []
        n = len(video_words)
        
        start_idx = 0
        known_count = 0
        total_count = 0

        for end_idx in range(n):
            # Add the current word to the counts
            word_id = video_words[end_idx]['root_word']
            total_count += 1
            if word_id in known_words:
                known_count += 1

            # Shrink the window if the percentage drops below the threshold
            while start_idx <= end_idx:
                current_percentage = (known_count / total_count) * 100
                if current_percentage >= percentage:
                    # Valid section found
                    start_time = float(video_words[start_idx]['start'])
                    end_time = float(video_words[end_idx]['end'])
                    duration = end_time - start_time

                    # Add the section with duration
                    video_sections.append((video.id, start_time, end_time, duration))
                    break
                else:
                    # Slide the window forward by excluding the start word
                    start_word_id = video_words[start_idx]['root_word']
                    total_count -= 1
                    if start_word_id in known_words:
                        known_count -= 1
                    start_idx += 1

        sections.extend(video_sections)
        
    sections = sorted(sections, key=lambda x: x[3], reverse=True)
        
    result = []
    global_last_end = {}

    for video_index, start_time, end_time, _ in sections:
        if video_index not in global_last_end or start_time >= global_last_end[video_index]:
            result.append((video_index, start_time, end_time))
            global_last_end[video_index] = end_time
            if len(result) == count:
                break

    return result
