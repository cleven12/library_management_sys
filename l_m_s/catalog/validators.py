from django.core.exceptions import ValidationError

def validate_isbn(value):
    """
    Validate ISBN-10 or ISBN-13 format.
    """
    isbn = value.replace('-', '').replace(' ', '')
    
    if len(isbn) == 10:
        return validate_isbn10(isbn)
    elif len(isbn) == 13:
        return validate_isbn13(isbn)
    else:
        raise ValidationError('ISBN must be 10 or 13 digits')

def validate_isbn10(isbn):
    if not isbn[:-1].isdigit():
        raise ValidationError('Invalid ISBN-10 format')
    
    check_digit = isbn[-1]
    if check_digit != 'X' and not check_digit.isdigit():
        raise ValidationError('Invalid ISBN-10 check digit')
    
    total = sum((10 - i) * int(digit) for i, digit in enumerate(isbn[:-1]))
    
    if check_digit == 'X':
        total += 10
    else:
        total += int(check_digit)
    
    if total % 11 != 0:
        raise ValidationError('Invalid ISBN-10 checksum')
    
    return isbn

def validate_isbn13(isbn):
    if not isbn.isdigit():
        raise ValidationError('Invalid ISBN-13 format')
    
    total = sum(
        int(digit) * (1 if i % 2 == 0 else 3)
        for i, digit in enumerate(isbn[:-1])
    )
    
    check_digit = (10 - (total % 10)) % 10
    
    if check_digit != int(isbn[-1]):
        raise ValidationError('Invalid ISBN-13 checksum')
    
    return isbn

def clean_isbn(isbn):
    """Remove hyphens and spaces from ISBN"""
    return isbn.replace('-', '').replace(' ', '')

def format_isbn(isbn):
    """Format ISBN with proper hyphens"""
    isbn = clean_isbn(isbn)
    
    if len(isbn) == 10:
        return f"{isbn[0]}-{isbn[1:6]}-{isbn[6:9]}-{isbn[9]}"
    elif len(isbn) == 13:
        return f"{isbn[0:3]}-{isbn[3]}-{isbn[4:9]}-{isbn[9:12]}-{isbn[12]}"
    
    return isbn
