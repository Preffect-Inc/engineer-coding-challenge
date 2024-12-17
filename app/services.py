from .models import User

def get_user_by_id(user_id):
    """
    Fetch a user by their ID.
    """
    try:
        return User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return None

def get_users_by_name(name):
    """
    Fetch users whose names match the given name (case-insensitive partial match).
    """
    return User.objects.filter(name__icontains=name)

def list_all_users():
    """
    Retrieve all users from the database.
    """
    return User.objects.all()
