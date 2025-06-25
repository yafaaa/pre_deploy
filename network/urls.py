from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all_posts/", views.all_posts, name="all_posts"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("following/", views.following, name="following"),  
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    path("toggle_like/<int:post_id>/", views.toggle_like, name="toggle_like"),
    path("add_comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("get_comments/<int:post_id>/", views.get_comments, name="get_comments"),
]
