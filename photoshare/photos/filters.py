import django_filters
from django_filters.filters import CharFilter

from .models import *


class PhotoFilter(django_filters.FilterSet):
    description = CharFilter(field_name='description', lookup_expr='icontains')
    category = CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Photo
        fields = '__all__'
        exclude = ['id','image', 'user', 'date_created']
