# Library Management System

Web-based application for managing library resources including books, members, loans, and more.

## Features

### Premium Features
- **Advanced User Management**: Multi-tier membership system (Standard, Premium, VIP, Student)
- **Comprehensive Catalog**: Books, authors, genres, publishers with full metadata
- **Smart Circulation**: Automated loan management, renewals, and reservations
- **Fine Management**: Automatic fine calculation with flexible policies
- **Notification System**: Email/SMS notifications with customizable preferences
- **Analytics Dashboard**: Real-time statistics and reporting for librarians
- **Book Reviews & Ratings**: Community-driven book recommendations
- **Reading Lists**: Personal and public reading list management
- **Search & Discovery**: Advanced search with filters and trending books
- **Activity Tracking**: Complete audit trail of all user actions
- **RESTful API**: JSON API for external integrations

### Technical Excellence
- Django 5.2.5 with Python 3
- SQLite database (easily upgradeable to PostgreSQL/MySQL)
- Responsive admin interface
- Automated management commands for daily operations
- Comprehensive test coverage
- Signal-based automation
- Export functionality (CSV reports)

## Installation

### Quick Setup
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Navigate to project
cd l_m_s

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Usage

### Access Points
- **Admin Panel**: http://localhost:8000/admin/
- **Member Portal**: http://localhost:8000/accounts/login/
- **Catalog**: http://localhost:8000/catalog/
- **API Endpoints**: http://localhost:8000/catalog/api/

### Management Commands
```bash
# Send due date reminders
python manage.py send_reminders

# Process overdue loans and generate fines
python manage.py process_overdue

# Update analytics and trending books
python manage.py update_analytics
```

## Apps Structure

### accounts
User authentication, member profiles, librarian management, activity logging

### catalog
Books, authors, genres, publishers, book instances, reviews, reading lists

### circulation
Loans, returns, renewals, reservations, fines, checkout policies

### notifications
Email/SMS notifications, user preferences, notification templates

### analytics
Book popularity tracking, member activity, library statistics, search analytics

### reports
Circulation reports, overdue tracking, revenue analysis, data exports

## Configuration

Key settings in `l_m_s/settings.py`:
- Database configuration
- Email backend settings
- Static files configuration
- Installed apps

## Testing

```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## License

See LICENSE file for details.

## Premium Highlights

- 6 Django apps with 20+ models
- 50+ views and API endpoints
- Advanced analytics and reporting
- Automated notification system
- Comprehensive test suites
- Production-ready architecture
