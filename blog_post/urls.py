from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.loginSession, name="login"),
    path("logout/", views.logoutSession, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.userProfile, name="profile"),
    path("edit_profile/", views.editProfile, name="edit_profile"),
    path("add_blog/", views.addBlogs, name="add_blog"),
    path("blog/<slug>/", views.blogDetail, name="blog_detail"),
    path("edit_blog/<id>/", views.editBlog, name="edit_blog"),
    path("user_profile/<id>/", views.guestProfile, name="user_profile"),
    path("delete_post/<id>/", views.deletePost, name="delete_post"),
    path("search_post/", views.searchPost, name="search_post"),
]
