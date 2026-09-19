from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from .models import (
    Reel,
    Message,
    Like,
    Comment,
    Follow,
    FollowRequest,
    DoctorProfile,
)


# =========================================================
# HOME
# =========================================================

def index(request):
    return render(request, 'index.html')


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.method == 'POST':

        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        phone_number = request.POST.get(
            'phone_number',
            ''
        ).strip()

        specialization = request.POST.get(
            'specialization',
            ''
        ).strip()

        qualification = request.POST.get(
            'qualification',
            ''
        ).strip()

        medical_registration_number = request.POST.get(
            'medical_registration_number',
            ''
        ).strip()

        # -------------------------------------------------
        # Check required fields
        # -------------------------------------------------

        if not name or not email or not password:

            messages.error(
                request,
                'Please fill all required fields.'
            )

            return redirect('register')

        # -------------------------------------------------
        # Check existing email
        # -------------------------------------------------

        if User.objects.filter(
            username__iexact=email
        ).exists():

            messages.error(
                request,
                'An account with this email already exists.'
            )

            return redirect('register')

        # -------------------------------------------------
        # Create Django User
        # -------------------------------------------------

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        # -------------------------------------------------
        # Create Doctor Profile
        # -------------------------------------------------

        DoctorProfile.objects.create(
            user=user,
            phone_number=phone_number,
            specialization=specialization,
            qualification=qualification,
            medical_registration_number=medical_registration_number
        )

        messages.success(
            request,
            'Registration successful! Please login.'
        )

        return redirect('login')

    return render(
        request,
        'register.html'
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == 'POST':

        email = request.POST.get(
            'email',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        # -------------------------------------------------
        # Check whether email was entered
        # -------------------------------------------------

        if not email or not password:

            messages.error(
                request,
                'Please enter your email and password.'
            )

            return redirect('login')

        # -------------------------------------------------
        # Find user using email
        # -------------------------------------------------

        user = User.objects.filter(
            email__iexact=email
        ).first()

        # -------------------------------------------------
        # Check password
        # -------------------------------------------------

        if user is not None and user.check_password(password):

            # Log the user in
            login(request, user)

            # Go to dashboard
            return redirect('dashboard')

        # -------------------------------------------------
        # Invalid login
        # -------------------------------------------------

        messages.error(
            request,
            'Invalid email or password.'
        )

        return redirect('login')

    return render(
        request,
        'login.html'
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect('index')


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    reels = Reel.objects.all().order_by('-id')

    return render(
        request,
        'dashboard.html',
        {
            'reels': reels,
        }
    )


# =========================================================
# DOCTORS
# =========================================================

@login_required
def doctors(request):

    doctors_list = DoctorProfile.objects.select_related(
        'user'
    ).all()

    return render(
        request,
        'doctors.html',
        {
            'doctors': doctors_list,
        }
    )


# =========================================================
# REELS
# =========================================================

@login_required
def reels(request):

    reels = Reel.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'reels.html',
        {
            'reels': reels,
        }
    )


# =========================================================
# UPLOAD REEL / MEDCLIP
# =========================================================

@login_required
def upload_reel(request):

    if request.method == 'POST':

        video = request.FILES.get('video')

        caption = request.POST.get(
            'caption',
            ''
        ).strip()

        # Check video
        if not video:

            messages.error(
                request,
                'Please select a video to upload.'
            )

            return redirect('upload_reel')

        # Create MedClip
        Reel.objects.create(
            doctor=request.user,
            video=video,
            caption=caption
        )

        messages.success(
            request,
            'MedClip uploaded successfully!'
        )

        return redirect('reels')

    return render(
        request,
        'upload_reel.html'
    )


# =========================================================
# LIKE REEL
# =========================================================

@login_required
def like_reel(request, reel_id):

    reel = get_object_or_404(
        Reel,
        id=reel_id
    )

    like = Like.objects.filter(
        user=request.user,
        reel=reel
    ).first()

    if like:

        like.delete()

    else:

        Like.objects.create(
            user=request.user,
            reel=reel
        )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'reels'
        )
    )


# =========================================================
# ADD COMMENT
# =========================================================

@login_required
def add_comment(request, reel_id):

    reel = get_object_or_404(
        Reel,
        id=reel_id
    )

    if request.method == 'POST':

        text = request.POST.get(
            'text',
            ''
        ).strip()

        if text:

            Comment.objects.create(
                user=request.user,
                reel=reel,
                text=text
            )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'reels'
        )
    )


# =========================================================
# DELETE COMMENT
# =========================================================

@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(
        Comment,
        id=comment_id
    )

    if comment.user == request.user:

        comment.delete()

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'reels'
        )
    )


# =========================================================
# PROFILE
# =========================================================

@login_required
def profile(request, user_id=None):

    # -----------------------------------------------------
    # If user_id is provided, show that user's profile
    # -----------------------------------------------------

    if user_id is not None:

        profile_user = get_object_or_404(
            User,
            id=user_id
        )

        profile_data, created = DoctorProfile.objects.get_or_create(
            user=profile_user
        )

    else:

        profile_user = request.user

        profile_data, created = DoctorProfile.objects.get_or_create(
            user=request.user
        )

    return render(
        request,
        'profile.html',
        {
            'profile': profile_data,
            'profile_user': profile_user,
        }
    )


# =========================================================
# FOLLOW USER
# =========================================================

@login_required
def follow_user(request, user_id):

    target_user = get_object_or_404(
        User,
        id=user_id
    )

    if target_user == request.user:

        return redirect(
            'profile_user',
            user_id=user_id
        )

    # Already following
    if Follow.objects.filter(
        follower=request.user,
        following=target_user
    ).exists():

        return redirect(
            'profile_user',
            user_id=user_id
        )

    # Check whether target is already following us
    if Follow.objects.filter(
        follower=target_user,
        following=request.user
    ).exists():

        Follow.objects.create(
            follower=request.user,
            following=target_user
        )

        return redirect(
            'profile_user',
            user_id=user_id
        )

    # Check existing pending request
    existing_request = FollowRequest.objects.filter(
        sender=request.user,
        receiver=target_user,
        status='pending'
    ).first()

    if existing_request:

        return redirect(
            'profile_user',
            user_id=user_id
        )

    # Create follow request
    FollowRequest.objects.create(
        sender=request.user,
        receiver=target_user,
        status='pending'
    )

    messages.success(
        request,
        'Follow request sent.'
    )

    return redirect(
        'profile_user',
        user_id=user_id
    )


# =========================================================
# UNFOLLOW USER
# =========================================================

@login_required
def unfollow_user(request, user_id):

    target_user = get_object_or_404(
        User,
        id=user_id
    )

    Follow.objects.filter(
        follower=request.user,
        following=target_user
    ).delete()

    return redirect(
        'profile_user',
        user_id=user_id
    )


# =========================================================
# CANCEL FOLLOW REQUEST
# =========================================================

@login_required
def cancel_follow_request(request, user_id):

    target_user = get_object_or_404(
        User,
        id=user_id
    )

    FollowRequest.objects.filter(
        sender=request.user,
        receiver=target_user,
        status='pending'
    ).delete()

    messages.success(
        request,
        'Follow request cancelled.'
    )

    return redirect(
        'profile_user',
        user_id=user_id
    )


# =========================================================
# FOLLOW REQUESTS
# =========================================================

@login_required
def follow_requests(request):

    requests = FollowRequest.objects.filter(
        receiver=request.user,
        status='pending'
    ).select_related(
        'sender'
    ).order_by('-id')

    return render(
        request,
        'profile.html',
        {
            'follow_requests': requests,
        }
    )


# =========================================================
# ACCEPT FOLLOW REQUEST
# =========================================================

@login_required
def accept_follow_request(request, request_id):

    follow_request = get_object_or_404(
        FollowRequest,
        id=request_id,
        receiver=request.user,
        status='pending'
    )

    Follow.objects.get_or_create(
        follower=follow_request.sender,
        following=request.user
    )

    follow_request.status = 'accepted'

    follow_request.save()

    messages.success(
        request,
        'Follow request accepted.'
    )

    return redirect(
        'follow_requests'
    )


# =========================================================
# REJECT FOLLOW REQUEST
# =========================================================

@login_required
def reject_follow_request(request, request_id):

    follow_request = get_object_or_404(
        FollowRequest,
        id=request_id,
        receiver=request.user,
        status='pending'
    )

    follow_request.status = 'rejected'

    follow_request.save()

    messages.success(
        request,
        'Follow request rejected.'
    )

    return redirect(
        'follow_requests'
    )


# =========================================================
# FOLLOWERS
# =========================================================

@login_required
def followers_list(request, user_id):

    target_user = get_object_or_404(
        User,
        id=user_id
    )

    followers = Follow.objects.filter(
        following=target_user
    ).select_related(
        'follower'
    )

    return render(
        request,
        'profile.html',
        {
            'profile_user': target_user,
            'followers': followers,
        }
    )


# =========================================================
# FOLLOWING
# =========================================================

@login_required
def following_list(request, user_id):

    target_user = get_object_or_404(
        User,
        id=user_id
    )

    following = Follow.objects.filter(
        follower=target_user
    ).select_related(
        'following'
    )

    return render(
        request,
        'profile.html',
        {
            'profile_user': target_user,
            'following': following,
        }
    )


# =========================================================
# MESSAGE LIST
# =========================================================

@login_required
def message_list(request):

    users = User.objects.exclude(
        id=request.user.id
    )

    return render(
        request,
        'messages.html',
        {
            'users': users,
        }
    )


# =========================================================
# CHAT
# =========================================================

@login_required
def chat(request, user_id):

    other_user = get_object_or_404(
        User,
        id=user_id
    )

    # -----------------------------------------------------
    # Send message
    # -----------------------------------------------------

    if request.method == 'POST':

        content = request.POST.get(
            'content',
            ''
        ).strip()

        if content:

            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )

        return redirect(
            'chat',
            user_id=user_id
        )

    # -----------------------------------------------------
    # Get conversation
    # -----------------------------------------------------

    chat_messages = Message.objects.filter(
        Q(
            sender=request.user,
            receiver=other_user
        )
        |
        Q(
            sender=other_user,
            receiver=request.user
        )
    ).order_by('id')

    return render(
        request,
        'chat.html',
        {
            'other_user': other_user,
            'chat_messages': chat_messages,
        }
    )