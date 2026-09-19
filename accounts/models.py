from django.db import models
from django.contrib.auth.models import User


# =========================================================
# DOCTOR PROFILE
# =========================================================

class DoctorProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    specialization = models.CharField(
        max_length=100,
        blank=True
    )

    qualification = models.CharField(
        max_length=100,
        blank=True
    )

    medical_registration_number = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.user.first_name or self.user.username


# =========================================================
# REEL
# =========================================================

class Reel(models.Model):

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reels'
    )

    caption = models.TextField(
        blank=True
    )

    video = models.FileField(
        upload_to='reels/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Keep this field because it already exists in your project.
    # It stores the number of likes.
    likes = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.doctor.username} - {self.caption}"


# =========================================================
# MESSAGE
# =========================================================

class Message(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"


# =========================================================
# FOLLOW REQUEST
# =========================================================

class FollowRequest(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_follow_requests'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_follow_requests'
    )

    accepted = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sender', 'receiver'],
                name='unique_follow_request'
            )
        ]

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"


# =========================================================
# FOLLOW
# =========================================================

class Follow(models.Model):

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


# =========================================================
# LIKE
# =========================================================

class Like(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reel_likes'
    )

    reel = models.ForeignKey(
        Reel,
        on_delete=models.CASCADE,
        related_name='like_records'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'reel'],
                name='unique_reel_like'
            )
        ]

    def __str__(self):
        return f"{self.user.username} liked Reel {self.reel.id}"


# =========================================================
# COMMENT
# =========================================================

class Comment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reel_comments'
    )

    reel = models.ForeignKey(
        Reel,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username}: {self.text}"