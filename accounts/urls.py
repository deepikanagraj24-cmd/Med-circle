from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        '',
        views.index,
        name='index'
    ),


    # =====================================================
    # AUTHENTICATION
    # =====================================================

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),


    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),


    # =====================================================
    # DOCTORS
    # =====================================================

    path(
        'doctors/',
        views.doctors,
        name='doctors'
    ),


    # =====================================================
    # REELS
    # =====================================================

    path(
        'reels/',
        views.reels,
        name='reels'
    ),

    path(
        'reels/upload/',
        views.upload_reel,
        name='upload_reel'
    ),

    path(
        'reels/<int:reel_id>/like/',
        views.like_reel,
        name='like_reel'
    ),

    path(
        'reels/<int:reel_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),

    path(
        'comments/<int:comment_id>/delete/',
        views.delete_comment,
        name='delete_comment'
    ),


    # =====================================================
    # PROFILE
    # =====================================================

    # Own profile
    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    # Other user's profile
    path(
        'profile/<int:user_id>/',
        views.profile,
        name='profile_user'
    ),


    # =====================================================
    # FOLLOW
    # =====================================================

    path(
        'follow/<int:user_id>/',
        views.follow_user,
        name='follow_user'
    ),

    path(
        'unfollow/<int:user_id>/',
        views.unfollow_user,
        name='unfollow_user'
    ),

    path(
        'follow/cancel/<int:user_id>/',
        views.cancel_follow_request,
        name='cancel_follow_request'
    ),


    # =====================================================
    # FOLLOW REQUESTS
    # =====================================================

    path(
        'follow-requests/',
        views.follow_requests,
        name='follow_requests'
    ),

    path(
        'follow-requests/<int:request_id>/accept/',
        views.accept_follow_request,
        name='accept_follow_request'
    ),

    path(
        'follow-requests/<int:request_id>/reject/',
        views.reject_follow_request,
        name='reject_follow_request'
    ),


    # =====================================================
    # FOLLOWERS / FOLLOWING
    # =====================================================

    path(
        'followers/<int:user_id>/',
        views.followers_list,
        name='followers_list'
    ),

    path(
        'following/<int:user_id>/',
        views.following_list,
        name='following_list'
    ),


    # =====================================================
    # MESSAGES
    # =====================================================

    path(
        'messages/',
        views.message_list,
        name='messages'
    ),

    path(
        'messages/<int:user_id>/',
        views.chat,
        name='chat'
    ),

]