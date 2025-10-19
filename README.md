# ALX Capstone Project 
## Task Manager API

### Overview
This is a Django REST Framework (DRF) backend project for managing tasks.  
Users can create, read, update, delete, and mark tasks as complete or incomplete.  
The project is designed as a learning backend project and includes user authentication, task ownership, and API endpoints for task management.

### Features
- CRUD operations for tasks
- Mark tasks as complete or incomplete
- User authentication (Django built-in)
- Task ownership: users can only access their own tasks
- Filtering and sorting tasks by priority, status, and due date
- Optional: categories, recurring tasks, collaborative tasks

---

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<your-username>/taskmanager-api.git
   cd taskmanager-api
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Mac/Linux
   env\Scripts\activate     # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Server**
   ```bash
   python manage.py runserver
   ```

Access the API at:
`http://127.0.0.1:8000/`

---

### API Authentication

**Obtain JWT token:**  
POST `/api/token/`
```json
{
  "username": "tsion",
  "password": "0000"
}
```

Use it in headers:  
```
Authorization: Bearer <your-token>
```

---

### API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | /api/register/ | Register a new user |
| POST | /api/token/ | Get JWT tokens |
| POST | /api/token/refresh/ | Refresh JWT token |
| GET | /api/tasks/ | List all user tasks |
| POST | /api/tasks/ | Create a new task |
| GET | /api/tasks/<id>/ | Retrieve a task |
| PUT | /api/tasks/<id>/ | Update a task |
| DELETE | /api/tasks/<id>/ | Delete a task |
| PATCH | /api/tasks/<id>/complete/ | Mark as complete/incomplete |

---

### Sample Data

#### Users
```json
{
  "username": "tsion",
  "email": "tsion@example.com",
  "password": "0000"
}
{
  "username": "john",
  "email": "john@example.com",
  "password": "pass123"
}
{
  "username": "sara",
  "email": "sara@example.com",
  "password": "pass456"
}
```

#### Token Requests
```json
{
  "username": "tsion",
  "password": "0000"
}
{
  "username": "john",
  "password": "pass123"
}
{
  "username": "sara",
  "password": "pass456"
}
```

#### Tasks
```json
{
  "title": "Finish API Documentation",
  "description": "Write detailed Postman tests and update README",
  "priority": "High",
  "status": "Pending",
  "due_date": "2025-10-25T12:00:00Z"
}
{
  "title": "Fix Login Bug",
  "description": "JWT token not refreshing automatically",
  "priority": "Medium",
  "status": "Pending",
  "due_date": "2025-10-22T09:00:00Z"
}
{
  "title": "Prepare Weekly Report",
  "description": "Summarize project progress for the week",
  "priority": "Low",
  "status": "Pending",
  "due_date": "2025-10-18T15:30:00Z"
}
```

---

### Project Structure
```
ALX_Task_manager/
│
├── manage.py
├── requirements.txt
├── taskmanager/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── tasks/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── permissions.py
    ├── urls.py
    └── tests.py
```
### Deployment 
Deploy on render.com 
**Link(Available at):** https://django-render-taskmanager-app.onrender.com/api/users/

### Author
**Name:** Tsion Feleke  
**Project:** ALX Capstone – Task Manager API  
**GitHub:** [github.com/theluchadora](https://github.com/theluchadora)  


---

### License
This project is open-source and available
