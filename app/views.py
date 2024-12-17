from django.http import JsonResponse
from .services import get_user_by_id, get_users_by_name, list_all_users

def user_by_id_or_name(request):
    """
    Retrieve a user by ID or by name using query parameters.
    URL: /users/filter/?id=<user_id>
    URL: /users/filter/?name=<user_name>
    """
    user_id = request.GET.get('id')  # Extract 'id' query parameter
    name = request.GET.get('name')   # Extract 'name' query parameter

    if user_id:
        # Get user by ID
        user = get_user_by_id(user_id)
        if user:
            return JsonResponse({
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "signup_date": user.signup_date,
                "age": user.age,
                "height_cm": user.height_cm,
                "weight_kg": user.weight_kg,
                "activity_level": user.activity_level,
                "health_goals": user.health_goals
            })
        return JsonResponse({"error": "User not found"}, status=404)

    elif name:
        # Get users by name (partial match)
        users = get_users_by_name(name)
        users_data = list(users.values())  # Serialize query results
        return JsonResponse(users_data, safe=False)

    # If no query parameters are provided
    return JsonResponse({"error": "Please provide 'id' or 'name' as query parameters"}, status=400)

def list_users(request):
    """
    List all users.
    URL: /users/
    """
    users = list_all_users()
    users_data = list(users.values())
    return JsonResponse(users_data, safe=False)
