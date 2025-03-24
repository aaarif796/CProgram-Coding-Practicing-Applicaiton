# Django Project

A web-based platform that allows users to register, log in, and access coding-related features. The platform is built using Django and provides an interactive experience for users.

## Features
- User authentication (register, login, logout)
- Questions and challenges for coding practice
- Track progress of completed and pending challenges
- Admin panel for user and content management

## Installation

Follow the steps below to set up the project locally.

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Apply Migrations
```sh
python manage.py migrate
```

### 5. Create a Superuser (Optional, for Admin Panel)
```sh
python manage.py createsuperuser
```

### 6. Run the Server
```sh
python manage.py runserver
```

Now, visit `http://127.0.0.1:8000/` in your browser to access the application.

## Usage
- Register/Login to access the platform.
- Navigate through coding challenges and track progress.
- Admins can log in to the `/admin/` panel for management.

## License
This project is open-source and available under the [MIT License](LICENSE).
