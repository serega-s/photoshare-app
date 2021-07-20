from django.shortcuts import redirect, render

from .forms import PhotoForm
from .models import Category, Photo


def gallery(request):
    categories = Category.objects.all()
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)
        
    context = {
        'photos': photos,
        'categories': categories
    }
    return render(request, 'photos/gallery.html', context)

def view_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    context = {
        'photo': photo
    }
    return render(request, 'photos/photo.html', context)

def add_photo(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        print('data:', data)
        print('image:', image)

        if data['category'] != 'none':
            category = Category.objects.get(id=int(data['category']))

        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image
        )

        return redirect('gallery')
    context = {
        'categories': categories
    }
    return render(request, 'photos/add.html', context)
