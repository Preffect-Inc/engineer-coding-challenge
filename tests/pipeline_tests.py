from django.core.management import call_command
from unittest.mock import patch
from django.test import TestCase
from app.models import User

class PipelineTests(TestCase):
    def setUp(self):
        # Set up test users
        User.objects.create(
            user_id="123", name="John Doe", email="john@example.com",
            signup_date="2024-01-01", age=30, height_cm=180, weight_kg=75,
            activity_level="active", health_goals="stay fit"
        )
        User.objects.create(
            user_id="456", name="Jane Smith", email="jane@example.com",
            signup_date="2024-02-01", age=28, height_cm=170, weight_kg=65,
            activity_level="moderate", health_goals="lose weight"
        )

    @patch("app.management.commands.runpipeline.openai.ChatCompletion.create")
    @patch("app.management.commands.runpipeline.requests.post")
    def test_pipeline_success(self, mock_post, mock_openai):
        """
        Test the pipeline runs successfully and sends notifications.
        """
        # Mock OpenAI response
        mock_openai.return_value = {
            "choices": [{"message": {"content": "Stay hydrated!"}}]
        }

        # Mock notification endpoint response
        mock_post.return_value.status_code = 200

        # Trigger the management command
        call_command('runpipeline')

        # Assert OpenAI API was called
        self.assertEqual(mock_openai.call_count, 2)

        # Assert Notification endpoint was called
        self.assertEqual(mock_post.call_count, 2)

        # Assert that the 'message' in the payload is "Stay hydrated!"
        first_call_args = mock_post.call_args_list[0]  # Get the first call arguments
        payload = first_call_args.kwargs['json']  # Extract the JSON payload
        self.assertEqual(payload['name'], "John Doe")
        self.assertEqual(payload['message'], "Stay hydrated!")
