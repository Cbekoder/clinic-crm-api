import django_filters
from .models import ROLE_CHOICES, User

class UserFilter(django_filters.FilterSet):
    role = django_filters.ChoiceFilter(
        field_name='role',
        choices=ROLE_CHOICES,
        label='Role'
    )

    class Meta:
        model = User
        fields = ['role']
