# Contributing to Library Management System

Thank you for considering contributing to our Library Management System! This document provides guidelines for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the bug report template
3. Include detailed steps to reproduce
4. Provide system information
5. Add screenshots if applicable

### Suggesting Features

1. Check if the feature has been suggested
2. Use the feature request template
3. Explain the use case clearly
4. Describe expected behavior
5. Consider implementation complexity

### Pull Requests

#### Before Submitting
- Update documentation
- Add tests for new features
- Ensure all tests pass
- Follow the code style guide
- Update CHANGELOG.md

#### Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add: amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

#### Commit Message Format
```
<type>: <subject>

<body>

<footer>
```

Types:
- **Add**: New feature
- **Fix**: Bug fix
- **Update**: Update existing feature
- **Refactor**: Code refactoring
- **Docs**: Documentation changes
- **Test**: Adding tests
- **Style**: Code style changes

Examples:
```
Add: User authentication with OAuth2

Implemented OAuth2 authentication for Google and GitHub.
Added social account models and views.

Closes #123
```

### Code Style

#### Python
- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 120 characters
- Use meaningful variable names
- Add type hints where possible

```python
def calculate_fine(loan: Loan, policy: CheckoutPolicy) -> Decimal:
    """Calculate fine amount for overdue loan."""
    if not loan.is_overdue():
        return Decimal('0.00')
    
    days = loan.days_overdue()
    amount = days * policy.fine_per_day
    return min(amount, policy.max_fine_amount)
```

#### Django
- Use class-based views where appropriate
- Implement proper model validation
- Use Django ORM efficiently
- Add indexes to frequently queried fields

#### JavaScript
- Use modern ES6+ syntax
- Follow Airbnb style guide
- Add JSDoc comments

### Testing

#### Unit Tests
```python
class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123'
        )
    
    def test_book_creation(self):
        self.assertEqual(self.book.title, 'Test Book')
```

#### Integration Tests
```python
class LoanAPITest(APITestCase):
    def test_create_loan(self):
        response = self.client.post('/api/loans/', data)
        self.assertEqual(response.status_code, 201)
```

### Documentation

- Update README.md for user-facing changes
- Update DEVELOPER.md for technical changes
- Add docstrings to all functions
- Include code examples
- Keep API documentation current

### Review Process

1. **Automated Checks**
   - Linting
   - Tests
   - Coverage

2. **Code Review**
   - At least one approval required
   - Address all comments
   - Keep discussions focused

3. **Merge**
   - Squash commits if necessary
   - Update changelog
   - Close related issues

## Development Environment

### Required Tools
- Python 3.10+
- Git
- Redis
- PostgreSQL (optional)

### Setup
```bash
git clone https://github.com/cleven12/library_management_sys.git
cd library_management_sys
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### Running Tests
```bash
python manage.py test
coverage run --source='.' manage.py test
coverage report
```

### Code Quality
```bash
# Linting
flake8 .
pylint l_m_s

# Type checking
mypy l_m_s

# Security
bandit -r l_m_s
```

## Project Structure

```
l_m_s/
├── accounts/          # User management
├── catalog/           # Book catalog
├── circulation/       # Loans and fines
├── notifications/     # Notification system
├── analytics/         # Statistics
├── reports/           # Reporting
└── l_m_s/            # Configuration
```

## Key Areas for Contribution

### High Priority
- Performance optimization
- Test coverage improvement
- Documentation enhancement
- Bug fixes

### Feature Requests
- Mobile app integration
- Advanced search filters
- Book recommendation engine
- Multi-language support

### Technical Debt
- Code refactoring
- Database optimization
- API versioning
- Caching implementation

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Acknowledged in documentation

## Questions?

- Open an issue for questions
- Join our discussions
- Check existing documentation

Thank you for contributing!
