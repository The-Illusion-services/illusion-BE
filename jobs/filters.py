from django_filters import rest_framework as filters
from .models import Job

class JobFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    company = filters.CharFilter(lookup_expr='icontains')
    roles = filters.CharFilter(lookup_expr='icontains')
    location = filters.CharFilter(lookup_expr='icontains')
    min_salary = filters.NumberFilter(field_name='salary', lookup_expr='gte')
    max_salary = filters.NumberFilter(field_name='salary', lookup_expr='lte')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = Job
        fields = ['title', 'company','roles', 'location', 'min_salary', 'max_salary', 'created_after']
