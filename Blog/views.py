from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from Blog.models import Post , Comment , Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from Blog.forms import PostForm , CommentForm , ProfileForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
# Create your views here.


#create post
@login_required(login_url='/login/')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

#read
def home(request):
    query = request.GET.get('q')

    if query:
        post_list = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_at')
    else:
        post_list = Post.objects.all().order_by('-created_at')

    paginator = Paginator(post_list, 6)   # 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'home.html', {
        'posts': posts
    })

#update

@login_required(login_url='/login/')
def update_post(request, id):
    post = get_object_or_404(Post,id=id)
    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail',post.id)
    else:
        form = PostForm(instance=post)

    return render(request,'create_post.html',{'form': form})

# delete view

@login_required(login_url='/login/')
def delete_post(request, id):
    post = get_object_or_404(Post,id=id)
    if request.user == post.author:
        post.delete()
    return redirect('home')


#signup form
def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form=UserCreationForm()
    return render(request, 'register.html', {'form':form})

#logout view
def logout_view(request):
    logout(request)
    return redirect('login')

#post detail View

@login_required(login_url='/login/')
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()

    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', id=post.id)

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })



@login_required(login_url='/login/')
def like_post(request, id):
    post = get_object_or_404(Post, id=id)
    liked = False

    if request.user in post.likes.all():
        post.likes.remove(request.user)

    else:
        post.likes.add(request.user)
        liked = True

    data = {
        'liked': liked,
        'total_likes': post.total_likes()
    }

    return JsonResponse(data)

def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user_profile)
    posts = Post.objects.filter(author=user_profile).order_by('-created_at')
    return render(request, 'profile.html', {
        'user_profile': user_profile,
        'profile': profile,
        'posts': posts
    })


def edit_profile(request):
    profile,created= Profile.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form=ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form=ProfileForm(instance=profile)

    return render(request,'edit_profile.html', {'form':form})


@login_required(login_url='/login/')
def add_comment(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':

        text = request.POST.get('text')
        comment = Comment.objects.create(post=post, user=request.user, text=text)

        data = {
            'username': comment.user.username,
            'text': comment.text
        }
        return JsonResponse(data)





@login_required(login_url='/login/')
def save_post(request, id):
    post = get_object_or_404(Post,id=id)
    saved = False

    if request.user in post.saved_by.all():
        post.saved_by.remove(request.user)

    else:
        post.saved_by.add(request.user)
        saved = True
    data = {
        'saved': saved
    }
    return JsonResponse(data)

# save post page
@login_required(login_url='/login/')
def saved_posts(request):
    posts = request.user.saved_posts.all().order_by('-created_at')
    return render(request,'saved_posts.html',{'posts': posts})

