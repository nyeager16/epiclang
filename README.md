
# EpicLang

EpicLang is a Django-based web application designed to enhance language learning using the **comprehensible input** methodology. It currently supports **Polish** and aims to make language acquisition efficient and engaging through personalized video content, vocabulary tracking, and integrated flashcard reviews.

---

## Features

- **Polish Language Support**  
  Currently tailored for learning Polish, leveraging research into the "comprehensible input" technique, which involves providing language that is understandable but slightly above the learner's current level.
  
- **Word Tracking**  
  The app tracks words the user knows and uses this data to personalize learning.

- **Video Library with Comprehension Levels**  
  Users can:
  - View videos with a percentage of known words displayed.
  - Access a queue of video clips tailored to a specific comprehension percentage level of their choosing.

- **Spaced Repetition Flashcards**  
  Integrated flashcard reviews use a spaced repetition system (SRS) algorithm for optimal vocabulary retention.

- **Personalized Vocabulary Recommendations**  
  Suggests words to learn based on video data for efficient vocabulary acquisition.

- **YouTube Channel Integration**  
  Import videos from a YouTube channel with the command:  
  ```bash
  python manage.py ytimport [channel url] "pl"
  ```

- **Vocabulary in Context**  
  Allows users to skip to the location of new vocabulary in a video for contextual learning.

---

## Requirements

- Python 3.13+
- Django 5.1.3
- Docker (optional for containerization)
- PostgreSQL (optional for containerized database)

---

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/epiclang.git
   ```
2. Navigate to the project directory:
   ```bash
   cd epiclang
   ```
3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
4. Set up the database:
   ```bash
   python manage.py migrate
   ```
5. Download the Dictionary:
  Download the "Dictionary (SGJP)" from the following link: http://morfeusz.sgjp.pl/download/en
  Place the downloaded dictioary file in the data folder of the project directory
6. Import the dictionary data:
   ```bash
   python manage.py tabimport "[filepath]"
   ```
7. Start the development server:
   ```bash
   python manage.py runserver
   ```
8. (Optional) Import YouTube data:
   ```bash
   python manage.py ytimport [channel url] "pl"
   ```

---

## Disclaimer

**This project is shared for review and evaluation purposes only. It may not be copied, modified, or used in any way without prior permission.**

---

## License

No license is included. For usage inquiries, please contact Nathan Yeager at `nyeager16@gmail.com`.

