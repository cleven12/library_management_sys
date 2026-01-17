from django.test import TestCase
from django.contrib.auth.models import User
from catalog.models import Book, Author, Genre, Publisher, BookInstance, Review
from datetime import date

class BookModelTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name='John',
            last_name='Doe'
        )
        self.genre = Genre.objects.create(name='Fiction')
        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            country='USA'
        )
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            publisher=self.publisher,
            publication_date=date.today(),
            pages=300
        )
        self.book.authors.add(self.author)
        self.book.genres.add(self.genre)
    
    def test_book_creation(self):
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.isbn, '1234567890123')
        self.assertEqual(self.book.pages, 300)
    
    def test_book_string_representation(self):
        self.assertEqual(str(self.book), 'Test Book')
    
    def test_book_authors_relationship(self):
        self.assertIn(self.author, self.book.authors.all())

class BookInstanceTests(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name='Test', country='USA')
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            publisher=self.publisher,
            publication_date=date.today(),
            pages=200
        )
        self.instance = BookInstance.objects.create(
            book=self.book,
            unique_id='BOOK001',
            location='Shelf A1'
        )
    
    def test_instance_creation(self):
        self.assertEqual(self.instance.unique_id, 'BOOK001')
        self.assertEqual(self.instance.status, 'AVAILABLE')
        self.assertEqual(self.instance.condition, 'GOOD')
    
    def test_instance_string_representation(self):
        expected = f"{self.book.title} (BOOK001)"
        self.assertEqual(str(self.instance), expected)

class ReviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reviewer')
        self.publisher = Publisher.objects.create(name='Test', country='USA')
        self.book = Book.objects.create(
            title='Test Book',
            isbn='1234567890123',
            publisher=self.publisher,
            publication_date=date.today(),
            pages=200
        )
    
    def test_review_creation(self):
        review = Review.objects.create(
            book=self.book,
            user=self.user,
            rating=5,
            title='Great book!',
            content='Really enjoyed this book.'
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.title, 'Great book!')
