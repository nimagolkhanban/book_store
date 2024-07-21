# 📚 Book Recommendation System

A comprehensive book recommendation system using Django REST Framework and PostgreSQL. This project allows users to view and rate books, and receive personalized book recommendations based on their past ratings.

## 🌟 Features

- **🔒 User Authentication**: Secure login and access to the API using JWT.
- **📖 Book Management**: View a list of books along with their ratings.
- **⭐ Rating System**: Rate books on a scale of 1 to 5, update or delete ratings.
- **📚 Genre Filtering**: Filter books based on their genre.
- **🤖 Personalized Recommendations**: Receive book recommendations based on user's past ratings.

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

## 🛠️ Installation

### Prerequisites

- 🐍 Python 3.8+
- 🐘 PostgreSQL
- 🌐 Django 3.2+
- 🛠️ Django REST Framework
- 🔐 djangorestframework-simplejwt

### Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/nimagolkhanban/book_store.git
    cd book_store
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the database**:

    Update the `DATABASES` setting in `BookRecommendationSystem/settings.py` with your PostgreSQL credentials:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'your_db_host',
            'PORT': '5432',
        }
    }
    ```

5. **Run migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

7. **Start the development server**:
    ```bash
    python manage.py runserver
    ```

## 🚀 Usage

### Authentication

1. **Obtain JWT token**:
    ```bash
    POST /api/auth/login/
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

2. **Refresh JWT token**:
    ```bash
    POST /api/auth/token/refresh/
    {
        "refresh": "your_refresh_token"
    }
    ```

### Book Management

1. **List all books**:
    ```bash
    GET /api/books/list/
    ```

2. **Filter books by genre**:
    ```bash
    GET /api/books/?genre=<genre>
    ```

### Rating System

1. **Add or update a rating**:
    ```bash
    POST /api/books/review/add/
    {
        "book_id": <book_id>,
        "rating": <rating_value>
    }
    ```

2. **Delete a rating**:
    ```bash
    POST /api/books/review/delete/
    {
        "book_id": <book_id>
    }
    ```

### Recommendations

1. **Get book recommendations**:
    ```bash
    GET /api/recommendations/suggest/
    ```

## 📚 API Endpoints

- `POST /api/auth/login/` : User login to obtain JWT token.
- `POST /api/auth/token/refresh/` : Refresh JWT token.
- `GET /api/books/list/` : List all books.
- `GET /api/books/` : Filter books by genre.
- `POST /api/books/review/add/` : Add or update a book rating.
- `POST /api/books/review/delete/` : Delete a book rating.
- `GET /api/recommendations/suggest/` : Get book recommendations.
