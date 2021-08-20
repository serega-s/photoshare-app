import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView
from django_filters.views import FilterView

from .filters import PhotoFilter
from .forms import PhotoForm, ProfileForm
from .models import Category, Comment, Photo, Profile


class Gallery(FilterView):
    template_name = 'photos/gallery.html'
    queryset = Photo.objects.order_by('-date_created').all()
    filterset_class = PhotoFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo_filter'] = self.filterset
        context['photos'] = self.filterset.qs
        context['categories'] = Category.objects.all()

        return context


class UserGallery(FilterView):
    template_name = 'photos/gallery.html'
    queryset = Photo.objects.order_by('-date_created').all()
    filterset_class = PhotoFilter
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo_filter'] = self.filterset
        context['photos'] = self.filterset.qs
        context['categories'] = Category.objects.all()
        context['show_back'] = True
        context['username'] = self.kwargs['username']
        context['header'] = f'Photos by {self.kwargs["username"]}'

        return context


class ViewPhoto(DetailView):
    context_object_name = 'photo'
    template_name = 'photos/photo.html'
    queryset = Photo.objects.all()


class AddPhoto(LoginRequiredMixin, FormView):
    template_name = 'photos/add.html'
    form_class = PhotoForm
    success_url = '/'

    def form_valid(self, form):
        form_cd = form.cleaned_data
        data = self.request.POST

        if form_cd['category']:
            category = Category.objects.get(name=form_cd['category'])
        elif data['category_new']:
            category, created = Category.objects.get_or_create(
                name=data['category_new'])
        else:
            category = None

        form.save(commit=False)

        photo = Photo.objects.create(
            user=self.request.user,
            category=category,
            description=form_cd['description'],
            image=form_cd['image']
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


class AddComment(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)

        comment = Comment.objects.create(
            user=request.user,
            photo_id=int(data['form']['photo']),
            content=data['form']['comment'],
        )

        return JsonResponse('Comment Added', safe=False)


class UserProfile(LoginRequiredMixin, DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'photos/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = self.request.user.photos.order_by(
            '-date_created').all()[:5]

        return context


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


class Followers(DetailView):
    model = User
    template_name = 'photos/followers.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class Follows(DetailView):
    model = User
    template_name = 'photos/follows.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = 'photos/edit_profile.html'
    queryset = Profile.objects.all()
    form_class = ProfileForm
    context_object_name = 'profile'

    def get_object(self):
        return self.queryset.get(user=self.request.user)

    def form_valid(self, form):
        form_cd = form.cleaned_data
        profile = self.request.user.profile

        profile.card_image = form_cd['card_image']
        profile.avatar = form_cd['avatar']
        profile.bio = form_cd['bio']

        profile.save()

        return HttpResponseRedirect(profile.get_absolute_url())
