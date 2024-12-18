# Preffect Coding Challenge Description

In order to help us assess your skills as a developer and ability to navigate external services, please complete the exercise outlined below. We’re looking for demonstration of:
- Thoughtful product design with scalability in mind
- Clean, well-structured, and performant code
- Creativity in implementation
  
In case something is unclear or you have any questions regarding the task, please do not hesitate to contact us at ryanne@preffect.com

Happy coding!


## Overview

You have a Django-based project that already loads users from `data/users.csv` and exposes them at `/users/`. However, there’s a file `app/legacy_service.py` which contains messy, standalone logic for loading users, searching them, and serving them via a basic HTTP server. Your first task is to **refactor and integrate this legacy code into the Django application** in a clean, maintainable, and scalable way.

After refactoring:

1. Ensure all data access and user queries are handled via Django models or a proper service layer.
2. Remove global state and improve code structure.
3. Replace the legacy HTTP logic with Django views and URLs.

**Then**, add a **daily notification pipeline** that:
- Uses OpenAI’s API to generate a daily health message for each user.
- Sends that message to a mock external endpoint (e.g., `http://localhost:5001/notifications`).
- Each user should receive one daily notification from one of three categories:
  - Daily health reminders
  - Personalized health insights
  - Educational tips

Your pipeline can be triggered by a management command (e.g. `python manage.py runpipeline`).

**Additional Requirements:**
- Write tests (unit and/or integration) for the notification pipeline and the refactored user lookup logic.
- Integrate tests into the provided CI workflow.
- Provide a Dockerfile and ensure the project can run in a container.
- Document your solution, design decisions, and instructions for running the code and tests.

### Time Expectation
This exercise is scoped to about 4-8 hours. We do not expect a production-ready final product, but we want to see how you think and what trade-offs you make.

### Running the Base Project

```bash
pip install -r requirements.txt
python manage.py makemigrations app
python manage.py migrate
python manage.py load_users
python manage.py runserver
```


# **What Was Done**

This repository contains a Django-based application refactored and extended as part of the Preffect coding challenge. The solution demonstrates:
- Scalable and maintainable design.
- Clean, well-structured, and testable code.
- Integration with external services, including OpenAI and a mock notification endpoint.
  
### **1. Legacy Code Refactor**
The legacy user service in `app/legacy_service.py` was refactored and integrated into the Django application:
- **Data Access**: User data is now handled via Django models (`app.models.User`).
- **Service Layer**: User queries (`get_user_by_id`, `get_users_by_name`) were moved to a dedicated service layer for separation of concerns.
- **Views and URLs**: Replaced the legacy HTTP server with Django views and URL patterns:
  - `/users/`: Lists all users.
  - `/users/filter/?id=<user_id>`: Fetches a user by ID.
  - `/users/filter/?name=<name>`: Fetches users by name.

### **2. Daily Notification Pipeline**
A daily notification pipeline was implemented to:
- Use **OpenAI’s API** to generate personalized health messages.
- Send notifications to a mock external endpoint (`http://localhost:5001/notifications`).
- Categories for messages:
  1. Daily health reminders.
  2. Personalized health insights.
  3. Educational tips.

#### **Triggering the Pipeline**
The pipeline is triggered via a Django management command:
```bash
python manage.py runpipeline
```

### **3. Automated Tests**
Comprehensive tests were added to validate the refactored code and the pipeline:
- **Legacy Refactor Tests**:
  - Validated user query methods (`get_user_by_id`, `get_users_by_name`).
  - Verified endpoint responses for `/users/`, `/users/filter/?id=`, and `/users/filter/?name=`.
- **Pipeline Tests**:
  - Mocked OpenAI API to simulate health message generation.
  - Mocked notification endpoint to test payload delivery.
  - Verified the delivered messages.

Tests are integrated into the CI workflow to run automatically on push and pull requests to the `main` branch.

### **4. Continuous Integration**
The provided CI workflow was updated:
- Tests are triggered on:
  - Pushes to the `main` branch.
  - Pull requests targeting `main`.
- Uses `pytest` to run the test suite.

---

## **Design Decisions**
1. **Separation of Concerns**:
   - Data access was centralized in a service layer to decouple logic from views.
   - Refactored legacy code to use Django ORM for scalability and maintainability.

2. **Extensibility**:
   - Categories for notifications are configurable and can be expanded easily.
   - Used OpenAI's GPT-4o-mini model for improved response quality, offering better accuracy and efficiency compared to previous models.

3. **Testing**:
   - Mocked external dependencies to isolate the application logic.
   - Focused on critical areas: user queries and pipeline execution.

---

## **Instructions**

### **Run the Application**
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Load User Data**:
   ```bash
   python manage.py load_users
   ```

4. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

5. Access endpoints:
   - `/users/`: List all users.
   - `/users/filter/?id=<user_id>`: Fetch a user by ID.
   - `/users/filter/?name=<name>`: Fetch users by name.

---

### **Run the Notification Pipeline**
1. Start the mock server for notifications:
   ```bash
   python mock_server.py
   ```
2. Trigger the pipeline:
   ```bash
   python manage.py runpipeline
   ```

---

### **Run Tests**
1. Install test dependencies:
   ```bash
   pip install pytest pytest-django
   ```

2. Run the test suite:
   ```bash
   pytest
   ```

---

## **Project Structure**
```
app/
├── management/
│   ├── commands/
│   │   ├── load_users.py  # Load users
│   │   ├── runpipeline.py # Daily notification pipeline command
├── migrations/
├── legacy_service.py      # Legacy code
├── models.py              # User model
├── services.py            # User service layer
├── urls.py                # App URL definitions
├── views.py               # User endpoints
data/
├── users.csv              # Users list
project/
├── settings.py            # Django project settings
├── urls.py                # Django project main URLs
├── wsgi.py                # Django project WSGI config
tests/
├── pipeline_tests.py      # Tests for the notification pipeline
├── users_tests.py         # Tests for user queries and views
Dockerfile                 # Dockerfile for production
manage.py                  # Main management file
mock_server.py             # Mock external notification endpoint
pytest.ini                 # Pytest config
README.md                  # README
requirements.txt           # Project dependencies
```

---

## **Future Improvements**
- Implement Celery to schedule the pipeline as a periodic task.
- Add frontend support for viewing user details and notifications.

