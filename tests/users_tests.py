from django.test import TestCase, Client
from django.urls import reverse
from app.models import User

class UserViewTests(TestCase):
    def setUp(self):
        # Set up test client and test data
        self.client = Client()
        User.objects.create(
            user_id="123", name="John Doe", email="john@example.com",
            signup_date="2024-01-01", age=30, height_cm=180,
            weight_kg=75, activity_level="active", health_goals="stay fit"
        )
        User.objects.create(
            user_id="456", name="Jane Smith", email="jane@example.com",
            signup_date="2024-02-01", age=28, height_cm=170,
            weight_kg=65, activity_level="moderate", health_goals="lose weight"
        )

    def test_list_users(self):
        """Test listing all users."""
        response = self.client.get(reverse('list_users'))  # /users/
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0]['name'], "John Doe")
        self.assertEqual(json_data[1]['name'], "Jane Smith")

    def test_get_user_by_id_success(self):
        """Test retrieving a user by ID."""
        response = self.client.get(reverse('user_by_id_or_name'), {'id': '123'})  # /users/filter/?id=123
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['user_id'], '123')
        self.assertEqual(json_data['name'], 'John Doe')

    def test_get_user_by_id_not_found(self):
        """Test retrieving a user by ID that does not exist."""
        response = self.client.get(reverse('user_by_id_or_name'), {'id': '999'})  # /users/filter/?id=999
        self.assertEqual(response.status_code, 404)
        json_data = response.json()
        self.assertEqual(json_data['error'], "User not found")

    def test_get_users_by_name_success(self):
        """Test retrieving users by name (partial match)."""
        response = self.client.get(reverse('user_by_id_or_name'), {'name': 'Jane'})  # /users/filter/?name=Jane
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['name'], "Jane Smith")

    def test_get_users_by_name_no_results(self):
        """Test retrieving users by name where no match is found."""
        response = self.client.get(reverse('user_by_id_or_name'), {'name': 'NoMatch'})  # /users/filter/?name=NoMatch
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(len(json_data), 0)

    def test_missing_query_parameters(self):
        """Test error response when no query parameters are provided to filter path."""
        response = self.client.get(reverse('user_by_id_or_name'))  # /users/filter/ with no params
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertEqual(json_data['error'], "Please provide 'id' or 'name' as query parameters")
