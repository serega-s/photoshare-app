import json
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PhotoForm
from .models import Category, Comment, Photo


def gallery(request):
    categories = Category.objects.all()
    category = request.GET.get('category')
    if category:
        photos = Photo.objects.filter(
            category__name=category).order_by('-date_created')
    else:
        photos = Photo.objects.order_by('-date_created').all()

    context = {
        'photos': photos,
        'categories': categories
    }
    return render(request, 'photos/gallery.html', context)


def photos_by_user(request, name):
    photos = Photo.objects.filter(
        user__username=name).order_by('-date_created')

    context = {
        'photos': photos,
        'username': name
    }

    return render(request, 'photos/gallery_by.html', context)


def view_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    context = {
        'photo': photo
    }
    return render(request, 'photos/photo.html', context)


@login_required
def add_photo(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        data = request.POST

        if form.is_valid():
            form_cd = form.cleaned_data
            print(form_cd)

            if form_cd['category']:
                category = Category.objects.get(name=form_cd['category'])
            elif data['category_new']:
                category, created = Category.objects.get_or_create(
                    name=data['category_new'])
            else:
                category = None

            form.save(commit=False)

            photo = Photo.objects.create(
                category=category,
                description=form_cd['description'],
                image=form_cd['image']
            )
            return redirect('gallery')
    else:
        form = PhotoForm()

    context = {
        'categories': categories,
        'form': PhotoForm
    }
    return render(request, 'photos/add.html', context)


@login_required
def add_comment(request):
    data = json.loads(request.body)
    print(data)

    Comment.objects.create(
        user=request.user,
        photo_id=int(data['form']['photo']),
        content=data['form']['comment'],
    )
    return JsonResponse('Comment Added', safe=False)


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    photos = request.user.photos

    context = {
        'user': user,
        'photos': photos
    }

    return render(request, 'photos/profile.html', context)


@login_required
def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    request.user.profile.follows.add(user.profile)

    return redirect('profile', username=username)


@login_required
def unfollow_user(request, username):
    user = get_object_or_404(User, username=username)
    request.user.profile.follows.remove(user.profile)

    return redirect('profile', username=username)


def followers(request, username):
    user = get_object_or_404(User, username=username)

    context = {
        'user': user,
    }

    return render(request, 'photos/followers.html', context)

def follows(request, username):
    user = get_object_or_404(User, username=username)

    context = {
        'user': user,
    }

    return render(request, 'photos/follows.html', context)