import random
import requests
import openai
from django.core.management.base import BaseCommand
from app.models import User
from django.conf import settings

# Categories of health messages
CATEGORIES = [
    "Daily health reminders",
    "Personalized health insights",
    "Educational tips"
]

def generate_health_message(category, user):
    """
    Generate a health message for a user based on the selected category using OpenAI's chat model.
    """
    messages = [
        {"role": "system", "content": "You are a friendly health assistant providing daily health tips."},
        {"role": "user", "content": (
            f"Here is some information about the user:\n"
            f"Age: '{user.age}',\n"
            f"Weight in Kg: '{user.weight_kg}',\n"
            f"Height in Cm: '{user.height_cm}',\n"
            f"Activity level: '{user.activity_level}',\n"
            f"Health Goals: '{user.health_goals}'.\n"
            f"Generate a one-sentence, helpful, and motivating '{category}' message for the user."
        )}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=50,
            api_key=settings.OPENAI_API_KEY
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error generating health message: {e}")
        return "Stay healthy and take care of yourself!"


def send_notification(user, message, category):
    """
    Send the notification to the mock external endpoint.
    """
    payload = {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "message": message
    }
    try:
        response = requests.post(settings.NOTIFICATION_ENDPOINT, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"Notification sent successfully to {user.name} in {category} category")
        else:
            print(f"Failed to send notification to {user.name}: {response.status_code}")
    except Exception as e:
        print(f"Error sending notification to {user.name}: {e}")

class Command(BaseCommand):
    help = "Run the daily notification pipeline to send health messages to all users"

    def handle(self, *args, **options):
        self.stdout.write("Starting daily notification pipeline...")

        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.WARNING("No users found in the database."))
            return

        for user in users:
            # Distribute evenly
            category = random.choices(CATEGORIES, weights=[1, 1, 1], k=1)[0]
            message = generate_health_message(category, user)
            send_notification(user, message, category)

        self.stdout.write(self.style.SUCCESS("Daily notification pipeline completed successfully."))
