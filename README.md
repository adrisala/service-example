# service-example

A Django REST Framework service for Ansible Automation Platform

## Description

This is a Django REST Framework service created using the AAP Service Template.

## Features

- Django 5.2.7
- Django REST Framework
- Ready-to-use project structure
- Configured with development tools (black, flake8, isort, mypy)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/adrisala/service_example.git
cd service_example
```

2. Create and activate a virtual environment:
```bash
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
isort .
```

### Linting
```bash
flake8
mypy .
```

## License

MIT

## Author

adrisala
