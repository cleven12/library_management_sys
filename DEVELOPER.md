# Library Management System - Developer Guide

## Architecture Overview

### Backend Structure
```
l_m_s/
├── accounts/          # User management and authentication
├── catalog/           # Book catalog and resources
├── circulation/       # Loan and fine management
├── notifications/     # Notification system
├── analytics/         # Statistics and reporting
├── reports/           # Advanced reporting
└── l_m_s/            # Project configuration
```

### Key Technologies
- **Django 5.2.5**: Web framework
- **Django REST Framework**: API development
- **Celery**: Async task processing
- **Redis**: Cache and message broker
- **SQLite/PostgreSQL**: Database
- **Pillow**: Image processing

## Development Setup

### Prerequisites
```bash
Python 3.10+
pip
virtualenv
Redis (for Celery)
```

### Environment Setup
```bash
# Clone repository
git clone https://github.com/cleven12/library_management_sys.git
cd library_management_sys

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
cd l_m_s
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py populate_data
```

### Running Services

#### Django Development Server
```bash
python manage.py runserver
```

#### Celery Worker
```bash
celery -A l_m_s worker -l info
```

#### Celery Beat (Scheduled Tasks)
```bash
celery -A l_m_s beat -l info
```

## API Documentation

### Authentication
All API endpoints require authentication via API key:
```
X-API-Key: your-api-key
```

### Endpoints

#### Books
- `GET /api/books/` - List all books
- `GET /api/books/<id>/` - Get book details
- `GET /api/books/<id>/availability/` - Check availability

#### Loans
- `GET /api/loans/` - List user's loans
- `POST /api/loans/` - Create new loan
- `PUT /api/loans/<id>/renew/` - Renew loan

#### Members
- `GET /api/members/` - List members (librarian only)
- `GET /api/members/<id>/` - Get member details

### Response Format
```json
{
    "count": 100,
    "pages": 10,
    "current_page": 1,
    "results": [...]
}
```

## Database Models

### Core Models

#### MemberProfile
- User authentication integration
- Membership tiers (Standard, Premium, VIP, Student)
- Activity tracking
- Notification preferences

#### Book
- Full bibliographic metadata
- ISBN tracking
- Rating system
- Multi-author/genre support

#### BookInstance
- Physical copy tracking
- Status management
- Location tracking
- Condition monitoring

#### Loan
- Checkout/return tracking
- Renewal management
- Overdue detection
- Fine calculation

## Management Commands

### Daily Operations
```bash
# Send reminders for books due soon
python manage.py send_reminders

# Process overdue books and generate fines
python manage.py process_overdue

# Update analytics and trending books
python manage.py update_analytics
```

### Data Management
```bash
# Populate sample data
python manage.py populate_data

# Cleanup old notifications
python manage.py cleanup_notifications
```

## Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific App Tests
```bash
python manage.py test accounts
python manage.py test catalog
python manage.py test circulation
```

### Coverage Report
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Deployment

### Production Settings
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lms_db',
        'USER': 'lms_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files
```bash
python manage.py collectstatic
```

### Celery with Supervisor
```ini
[program:celery]
command=/path/to/venv/bin/celery -A l_m_s worker -l info
directory=/path/to/project
user=www-data
autostart=true
autorestart=true
```

## Security Considerations

- Always use HTTPS in production
- Set strong SECRET_KEY
- Enable CSRF protection
- Use environment variables for sensitive data
- Implement rate limiting
- Regular security updates

## Performance Optimization

### Database
- Add indexes on frequently queried fields
- Use select_related() and prefetch_related()
- Implement database query caching

### Caching
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### API Optimization
- Implement pagination
- Use serializers efficiently
- Add API response caching
- Implement throttling

## Contributing

### Code Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Write unit tests for new features

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add: new feature description"

# Push to GitHub
git push origin feature/new-feature

# Create pull request
```

## Troubleshooting

### Common Issues

#### Migration Conflicts
```bash
python manage.py migrate --fake <app_name> <migration_name>
python manage.py migrate
```

#### Celery Not Running
```bash
# Check Redis connection
redis-cli ping

# Restart Celery
pkill -9 celery
celery -A l_m_s worker -l info
```

#### Static Files Not Loading
```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/cleven12/library_management_sys/issues
- Documentation: README.md
- Developer Guide: DEVELOPER.md
