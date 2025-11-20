# Library Management System

## Overview
A comprehensive web-based Library Management System built with Django 5.2.5 and styled with Bootstrap 5.3.0. This application manages library resources including books, authors, members, and circulation (loans and reservations).

## Project Status
- **Current State**: Fully functional with all core apps implemented
- **Last Updated**: November 18, 2025
- **Framework**: Django 5.2.5
- **Frontend**: Bootstrap 5.3.0 CSS
- **Database**: SQLite3 (development)

## Project Architecture

### Django Apps

#### 1. **accounts** - User & Member Management
- **Models**: MemberProfile (extends Django User)
- **Features**: 
  - Member profiles with status tracking (Active, Suspended, Expired)
  - Member ID, contact info, and membership dates
  - Integration with Django authentication

#### 2. **catalog** - Library Collection Management
- **Models**: Author, Genre, Book, BookInstance
- **Features**:
  - Comprehensive book catalog with ISBN, publisher, publication dates
  - Many-to-many relationships for authors and genres
  - Individual book copy (instance) tracking with status
  - Book and author detail pages
  - Search and filtering capabilities

#### 3. **circulation** - Loan & Reservation Management
- **Models**: Loan, Reservation
- **Features**:
  - Book checkout/checkin system
  - Automatic due date calculation (14 days)
  - Overdue tracking with fine calculation ($0.50/day)
  - Reservation queue system with expiry dates
  - User-specific loan viewing

#### 4. **reports** - Analytics & Reporting
- **Models**: None (queries other apps' data)
- **Features**:
  - Dashboard with library statistics
  - Most borrowed books report
  - Circulation statistics (last 7/30 days)
  - Overdue items tracking
  - Staff-only access with permission checks

## Key Features

### User Interface
- Clean, modern Bootstrap 5.3.0 design
- Responsive navigation with dropdown menus
- Dashboard with colorful statistic cards
- List views with pagination
- Detail views for books and authors

### Admin Interface
- Full Django admin customization
- Custom list displays and filters
- Inline editing for related models
- Search functionality

### Authentication
- Built-in Django authentication
- Login/logout functionality
- Permission-based access control
- Staff/librarian role management

## File Structure
```
l_m_s/
├── l_m_s/              # Main project configuration
│   ├── settings.py     # Django settings (ALLOWED_HOSTS = ['*'])
│   ├── urls.py         # URL routing
│   └── wsgi.py        
├── accounts/           # User & member management app
│   ├── models.py       # MemberProfile model
│   └── admin.py        # Admin configuration
├── catalog/            # Library catalog app
│   ├── models.py       # Book, Author, Genre, BookInstance
│   ├── views.py        # List and detail views
│   ├── urls.py         # App URL patterns
│   └── admin.py        # Admin configuration
├── circulation/        # Loan & reservation app
│   ├── models.py       # Loan, Reservation models
│   └── admin.py        # Admin configuration
├── reports/            # Analytics app (future)
├── templates/          # HTML templates
│   ├── base_generic.html     # Bootstrap base template
│   ├── catalog/              # Catalog templates
│   └── registration/         # Auth templates
└── manage.py           # Django management script
```

## Configuration

### Dev Env Settings
- **Host**: 0.0.0.0:5000 (frontend)
- **ALLOWED_HOSTS**: ['*'] for Dev Env proxy compatibility
- **DEBUG**: True (development mode)

### Database
- SQLite3 for development
- Migrations applied for all apps

### Static Files
- Bootstrap 5.3.0 via CDN
- Bootstrap Icons included
- STATIC_ROOT configured for deployment

## URLs
- `/` - Redirects to catalog home
- `/catalog/` - Library home with statistics
- `/catalog/books/` - Book list
- `/catalog/book/<id>/` - Book detail
- `/catalog/authors/` - Author list
- `/catalog/author/<id>/` - Author detail
- `/catalog/mybooks/` - User's borrowed books (login required)
- `/accounts/login/` - Login page
- `/admin/` - Django admin interface

## Getting Started

### Creating a Superuser
```bash
cd l_m_s
python manage.py createsuperuser
```

### Adding Sample Data
Use the Django admin at `/admin/` to:
1. Add authors
2. Add genres
3. Add books
4. Create book instances (copies)
5. Create member profiles

## Deployment
- **Target**: Autoscale deployment
- **Server**: Gunicorn with WSGI
- **Build**: pip install requirements
- **Run**: Migrations + collectstatic + gunicorn

## Future Enhancements
- Reports app with analytics
- Email notifications for due dates
- Advanced search and filtering
- Book reservations queue management
- Member registration page
- Fine payment tracking
