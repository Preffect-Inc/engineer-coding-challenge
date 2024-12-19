from django.urls import path
from .views import user_by_id_or_name, list_users

urlpatterns = [
    path('', list_users, name='list_users'),
    path('filter/', user_by_id_or_name, name='user_by_id_or_name'),  # Get user by ID or name
]