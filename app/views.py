from django.shortcuts import get_object_or_404, render,redirect

from app.models import  Post, Tag, WebsiteMeta
from app.forms import CommentForm, NewUserForm, SubscribeForm
from app.models import Comments
from app.models import Profile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import login

# Create your views here.

def index(request):
    posts = Post.objects.all()
    top_post=Post.objects.order_by('-view_count')[:3]
    recent_post=Post.objects.order_by('-last_updated')[:3]
    featured_blog = Post.objects.filter(is_featured=True)
    subscribe_form = SubscribeForm()
    subscribe_successful = None
    website_meta = None
    
    if WebsiteMeta.objects.all().exists():
        website_meta = WebsiteMeta.objects.all()[0]
    
    if featured_blog:
        featured_blog = featured_blog[0]  # Get the first featured blog if exists
    
    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            request.session['subscribed'] = True
            request.session['subscribe_successful'] = 'Subscription successful!'
            return HttpResponseRedirect(reverse('index'))
        
    if 'subscribe_successful' in request.session:
        subscribe_successful = request.session.pop('subscribe_successful')

    context = {'posts': posts,'top_post':top_post,'recent_post':recent_post,'subscribe_form':subscribe_form,'subscribe_successful':subscribe_successful, 'featured_blog':featured_blog, 'website_meta': website_meta}
    return render(request, 'app/index.html', context)

def post_page(request,slug):
    post = Post.objects.get(slug=slug)
    comments=Comments.objects.filter(post=post,parent=None)
    form =CommentForm()
    
    #Bookmark logic
    post = get_object_or_404(Post, slug=slug)
    is_bookmarked = post.bookmarks.filter(id=request.user.id).exists() if request.user.is_authenticated else False
    
    #like logic
    post = get_object_or_404(Post, slug=slug)
    number_of_likes = post.number_of_likes()
    is_liked = post.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False
    
    #comments logic
    post= get_object_or_404(Post, slug=slug)
    number_of_comments = post.number_of_comments()
    is_comments = post.comments.filter(id=request.user.id).exists() if request.user.is_authenticated else False

    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            parent_comment = None
            if request.POST.get('parent'):
                parent_id = request.POST.get('parent')
                parent_comment = Comments.objects.get(id=parent_id)
                if parent_comment:
                    comment_reply = form.save(commit=False)
                    comment_reply.post = post
                    comment_reply.parent = parent_comment
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
            else:
                comment = form.save(commit=False)
                post_id = request.POST.get('post_id')
                post=Post.objects.get(id=post_id)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))


    post.view_count += 1
    post.save()
    
    #sidebar
    recent_posts=Post.objects.exclude(id=post.id).order_by('-last_updated')[:3]
    top_authors=User.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:3]
    tags=Tag.objects.all()
    related_posts = Post.objects.exclude(id=post.id).filter(author=post.author)[:3]


    context={'post':post,'form':form, 'comments':comments, 'is_bookmarked': is_bookmarked, 'is_liked': is_liked, 'number_of_likes': number_of_likes, 'number_of_comments': number_of_comments, 'is_comments': is_comments, 'recent_posts': recent_posts, 'top_authors': top_authors, 'tags': tags, 'related_posts': related_posts}
    return render(request,'app/post.html',context)

def tag_page(request,slug):
    tag=Tag.objects.get(slug=slug)

    top_post=Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[:3]
    recent_post=Post.objects.filter(tags__in=[tag.id]).order_by('-last_updated')[:3]
    tags=Tag.objects.all()
    context={'tag':tag,'top_post':top_post,'recent_post':recent_post,'tags':tags}
    return render(request,'app/tag.html',context)

def author_page(request,slug):
    profile=Profile.objects.get(slug=slug)

    top_post=Post.objects.filter(author=profile.user).order_by('-view_count')[:3]
    recent_post=Post.objects.filter(author=profile.user).order_by('-last_updated')[:3]
    
    top_authors=User.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:3]

    context={'profile':profile,'top_post':top_post,'recent_post':recent_post,'top_authors':top_authors}
    return render(request,'app/author.html',context)

def search_post(request):
    search_query = ''
    if request.GET.get('q'):
        search_query = request.GET.get('q')

    results = Post.objects.filter(title__icontains=search_query)
    context = { 'results': results, 'search_query': search_query }
    return render(request, 'app/search.html', context)

def about(request):
    website_meta = None
    
    if WebsiteMeta.objects.all().exists():
        website_meta = WebsiteMeta.objects.all()[0]
        
    context={'website_meta': website_meta}
    return render(request, 'app/about.html',context)

def logout_page(request):
    return render(request, 'app/logout.html')

def register_user(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
            
    context={'form': form}
    return render(request, 'registration/registration.html', context)

def bookmarks_post(request, slug):
    post=get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

def like_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

def all_bookmarked_posts(request):
    bookmarked_posts = Post.objects.filter(bookmarks=request.user)
    context = {'bookmarked_posts': bookmarked_posts}
    return render(request, 'app/all_bookmarked_posts.html', context)


def all_posts(request):
    all_posts = Post.objects.all()
    context = {'all_posts': all_posts}
    return render(request, 'app/all_posts.html', context)

def all_likes(request):
    liked_posts = Post.objects.filter(likes=request.user)
    context = {'liked_posts': liked_posts}
    return render(request, 'app/all_likes.html', context)