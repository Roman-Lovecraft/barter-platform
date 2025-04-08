# Barter Platform

This is a Django-based barter platform where users can exchange ads with each other. The project is structured to facilitate easy management of ads and user profiles.

## Features

- User registration and authentication
- Item listing and management
- Barter offers between users
- Admin panel for managing users and ads

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd barter-platform
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

- Access the application at `http://127.0.0.1:8000/`
- Admin panel can be accessed at `http://127.0.0.1:8000/admin/`

## Contributing

Feel free to submit issues or pull requests for improvements and bug fixes. 

## License

This project is licensed under the MIT License.