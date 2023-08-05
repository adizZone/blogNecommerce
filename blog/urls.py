from django.urls import path
from . import views

urlpatterns = [
    path("", views.blogHome, name="BlogHome"),
    path("blogs/", views.index, name='blogs'),
    path("messenger/", views.messenger, name='messenger'),
    
    # Try this using slug instead of id...
    path("BlogPost/<int:blg_id>", views.blogPost, name='BlogPost'),

    path("AddPost/", views.addPost, name="AddPost"),
    path("custom-post/", views.customPost, name="custom-post"),
    path("login/", views.handleLogin, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("sign_up/", views.handleSing_up, name="sign_up"),
    path("search_result/", views.search, name='search_result'),
    path("comments/", views.blogComment, name='comments')
]