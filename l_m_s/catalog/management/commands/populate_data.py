from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import MemberProfile
from catalog.models import Book, Author, Genre, Publisher, BookInstance
from circulation.models import CheckoutPolicy
from datetime import date
import random

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        genres = ['Fiction', 'Non-Fiction', 'Science Fiction', 'Mystery', 'Romance', 
                  'Thriller', 'Biography', 'History', 'Self-Help', 'Technology']
        genre_objects = []
        for genre_name in genres:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genre_objects.append(genre)
            if created:
                self.stdout.write(f'Created genre: {genre_name}')
        
        publishers_data = [
            ('Penguin Random House', 'USA'),
            ('HarperCollins', 'USA'),
            ('Simon & Schuster', 'USA'),
            ('Hachette', 'France'),
            ('Macmillan', 'UK'),
        ]
        publisher_objects = []
        for name, country in publishers_data:
            pub, created = Publisher.objects.get_or_create(
                name=name,
                defaults={'country': country}
            )
            publisher_objects.append(pub)
            if created:
                self.stdout.write(f'Created publisher: {name}')
        
        authors_data = [
            ('Stephen', 'King'), ('J.K.', 'Rowling'), ('George', 'Orwell'),
            ('Jane', 'Austen'), ('Mark', 'Twain'), ('Ernest', 'Hemingway'),
            ('Virginia', 'Woolf'), ('F. Scott', 'Fitzgerald'),
        ]
        author_objects = []
        for first, last in authors_data:
            author, created = Author.objects.get_or_create(
                first_name=first,
                last_name=last
            )
            author_objects.append(author)
            if created:
                self.stdout.write(f'Created author: {first} {last}')
        
        books_data = [
            ('The Great Gatsby', '9780743273565', 180),
            ('To Kill a Mockingbird', '9780061120084', 324),
            ('1984', '9780451524935', 328),
            ('Pride and Prejudice', '9780141439518', 432),
            ('The Catcher in the Rye', '9780316769174', 277),
            ('Animal Farm', '9780452284241', 112),
            ('Brave New World', '9780060850524', 288),
            ('The Hobbit', '9780547928227', 310),
        ]
        
        for title, isbn, pages in books_data:
            book, created = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    'title': title,
                    'publisher': random.choice(publisher_objects),
                    'publication_date': date(2020, 1, 1),
                    'pages': pages,
                    'language': 'EN',
                }
            )
            if created:
                book.authors.set([random.choice(author_objects)])
                book.genres.set(random.sample(genre_objects, 2))
                
                for i in range(3):
                    BookInstance.objects.create(
                        book=book,
                        unique_id=f'{isbn[-6:]}-{i+1:03d}',
                        barcode=f'BK{book.id:06d}-{i+1:03d}',
                        location=f'Shelf {chr(65+i)}{random.randint(1,9)}'
                    )
                self.stdout.write(f'Created book: {title} with 3 instances')
        
        policies = [
            ('STANDARD', 5, 14, 3, 0.50, 50.00),
            ('PREMIUM', 10, 21, 5, 0.25, 100.00),
            ('VIP', 20, 30, 10, 0.10, 200.00),
            ('STUDENT', 7, 14, 3, 0.50, 30.00),
        ]
        
        for membership_type, max_books, loan_days, max_renewals, fine_rate, max_fine in policies:
            policy, created = CheckoutPolicy.objects.get_or_create(
                membership_type=membership_type,
                defaults={
                    'max_books': max_books,
                    'loan_period_days': loan_days,
                    'max_renewals': max_renewals,
                    'fine_per_day': fine_rate,
                    'max_fine_amount': max_fine,
                }
            )
            if created:
                self.stdout.write(f'Created checkout policy: {membership_type}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
