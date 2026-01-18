from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from catalog.advanced_models import (
    BookRecommendation, ReadingChallenge, ChallengeParticipation,
    BookDiscussion, DiscussionComment, EBookFile
)
from catalog.models import Book
from accounts.models import MemberProfile

@login_required
def recommendations(request):
    profile = get_object_or_404(MemberProfile, user=request.user)
    recommendations = BookRecommendation.objects.filter(
        member=profile
    ).select_related('book')[:20]
    
    return render(request, 'catalog/recommendations.html', {
        'recommendations': recommendations
    })

@login_required
def reading_challenges(request):
    challenges = ReadingChallenge.objects.filter(
        is_active=True
    ).annotate(
        participants_count=Count('challengeparticipation')
    )
    
    profile = get_object_or_404(MemberProfile, user=request.user)
    my_challenges = ChallengeParticipation.objects.filter(
        member=profile
    ).select_related('challenge')
    
    return render(request, 'catalog/challenges.html', {
        'challenges': challenges,
        'my_challenges': my_challenges
    })

@login_required
def join_challenge(request, challenge_id):
    challenge = get_object_or_404(ReadingChallenge, id=challenge_id)
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    ChallengeParticipation.objects.get_or_create(
        challenge=challenge,
        member=profile
    )
    
    return redirect('reading_challenges')

@login_required
def book_discussions(request):
    discussions = BookDiscussion.objects.filter(
        is_active=True
    ).select_related('book', 'created_by').annotate(
        comments_count=Count('comments')
    )
    
    return render(request, 'catalog/discussions.html', {
        'discussions': discussions
    })

@login_required
def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(
        BookDiscussion.objects.select_related('book', 'created_by'),
        id=discussion_id
    )
    
    comments = DiscussionComment.objects.filter(
        discussion=discussion,
        parent__isnull=True
    ).select_related('user').prefetch_related('replies')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        comment = DiscussionComment.objects.create(
            discussion=discussion,
            user=request.user,
            content=content,
            parent_id=parent_id if parent_id else None
        )
        return redirect('discussion_detail', discussion_id=discussion_id)
    
    return render(request, 'catalog/discussion_detail.html', {
        'discussion': discussion,
        'comments': comments
    })

@login_required
def ebooks_library(request):
    ebooks = EBookFile.objects.filter(
        is_active=True
    ).select_related('book').order_by('-uploaded_at')
    
    search = request.GET.get('search', '')
    if search:
        ebooks = ebooks.filter(
            Q(book__title__icontains=search) |
            Q(book__authors__first_name__icontains=search) |
            Q(book__authors__last_name__icontains=search)
        ).distinct()
    
    format_filter = request.GET.get('format')
    if format_filter:
        ebooks = ebooks.filter(format=format_filter)
    
    return render(request, 'catalog/ebooks.html', {
        'ebooks': ebooks
    })

@login_required
def download_ebook(request, ebook_id):
    from catalog.advanced_models import EBookDownload
    from django.http import FileResponse
    
    ebook = get_object_or_404(EBookFile, id=ebook_id, is_active=True)
    
    EBookDownload.objects.create(
        ebook=ebook,
        user=request.user,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    ebook.downloads_count += 1
    ebook.save()
    
    return FileResponse(ebook.file, as_attachment=True)
