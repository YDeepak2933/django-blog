from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    posts = BlogPost.objects.filter().order_by("-dateTime")
    return render(request, "home.html", {"posts": posts})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            context = {
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "alert": True,
            }
            return render(request, "register.html", context)

        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, "login.html", {"success": True})
    return render(request, "register.html", {})


@login_required(login_url="/login")
def logoutSession(request):
    logout(request)
    return redirect("/")


def loginSession(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"success": False})
    return render(request, "login.html")


@login_required(login_url="/login")
def userProfile(request):
    return render(request, "profile.html")


@login_required(login_url="/login")
def editProfile(request):
    try:
        profile = request.user.profile
    except:
        profile = Profile(user=request.user)
    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, "profile.html", {"success": True})
    else:
        form = ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {"form": form})


@login_required(login_url="/login")
def editBlog(request, id):
    blog = BlogPost.objects.get(id=id)
    if request.method == "POST":
        form = BlogPostForm(data=request.POST, files=request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = BlogPostForm(instance=blog)
        success = False
    return render(
        request, "edit_blog.html", {"form": form, "blog": blog.id, "success": success}
    )


@login_required(login_url="/login")
def addBlogs(request):
    if request.method == "POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            return redirect("/")
    else:
        form = BlogPostForm()
    return render(request, "add_blog.html", {"form": form})


def blogDetail(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method == "POST":
        user = request.user
        content = request.POST.get("content", "")
        comment = Comment(user=user, content=content, blog=post)
        comment.save()
    return render(request, "blog_detail.html", {"post": post, "comments": comments})


def guestProfile(request, id):
    profile = Profile.objects.get(user=id)
    context = {"profile": profile}
    return render(request, "user_profile.html", context)


@login_required(login_url="/login")
def deletePost(request, id):
    blog = BlogPost.objects.get(id=id)
    blog.delete()
    return redirect("/")


def searchPost(request):
    query = request.GET.get("search")
    posts = BlogPost.objects.filter(title__icontains=query).order_by("-dateTime")
    return render(request, "home.html", {"posts": posts})
