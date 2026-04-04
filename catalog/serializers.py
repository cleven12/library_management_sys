from rest_framework import serializers
from catalog.models import Book, BookInstance, Author, Genre
from circulation.models import Loan, Fine
from accounts.models import MemberProfile

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'nationality', 'biography']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    available_copies = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'subtitle', 'isbn', 'publication_date',
            'pages', 'language', 'description', 'average_rating',
            'total_ratings', 'authors', 'genres', 'available_copies'
        ]
    
    def get_available_copies(self, obj):
        return obj.instances.filter(status='AVAILABLE').count()

class BookInstanceSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = BookInstance
        fields = ['id', 'unique_id', 'barcode', 'status', 'condition', 'location', 'book_title']

class LoanSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book_instance.book.title', read_only=True)
    member_name = serializers.CharField(source='member.user.get_full_name', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Loan
        fields = [
            'id', 'book_title', 'member_name', 'checkout_date',
            'due_date', 'return_date', 'status', 'renewal_count',
            'is_overdue'
        ]

class FineSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.user.get_full_name', read_only=True)
    
    class Meta:
        model = Fine
        fields = ['id', 'member_name', 'amount', 'reason', 'status', 'issued_date', 'paid_date']

class MemberProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = MemberProfile
        fields = [
            'id', 'username', 'email', 'full_name', 'member_id',
            'membership_type', 'status', 'membership_start'
        ]
