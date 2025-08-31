from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.index,name='index'),
    path('post/<slug:slug>/', views.post_page, name='post_page'),
    path('tag/<slug:slug>/', views.tag_page, name='tag_page'),
    path('author/<slug:slug>/', views.author_page, name='author_page'),
    path('search/', views.search_post, name='search'),
    path('about/', views.about, name='about'),
    path('logout/',views.logout_page, name='logout_page'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),  # Custom logout view
    path('accounts/register/', views.register_user, name='register'),
    path('bookmarks/<slug:slug>/', views.bookmarks_post, name='bookmarks_post'),
    path('like_post/<slug:slug>/', views.like_post, name='like_post'),
    path('all_bookmarked_posts/', views.all_bookmarked_posts, name='all_bookmarked_posts'),
    path('all_posts/', views.all_posts, name='all_posts'),
    path('all_likes/', views.all_likes, name='all_likes'),




]
