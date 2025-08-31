# 🐍 Django BlogApp (Basic Django Project)

A simple **Django project** with HTML templates and Python backend.  
This app demonstrates the fundamentals of Django: models, views, templates, static files, and basic authentication.  

---

## 🚀 Features
- 📝 Create, read, update, and delete posts  
- 👤 User registration & login system  
- 🖼️ HTML templates with Django template engine  
- 🎨 Static files handling (CSS/JS/images)  
- 🗄️ SQLite database (default, can be swapped for PostgreSQL/MySQL)  

---

## 🛠️ Tech Stack
- **Backend**: Django 5.x  
- **Frontend**: HTML, CSS (Django Templates)  
- **Database**: SQLite (default)  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/blogapp.git
cd blogapp

VIRTUAL ENVIORNMENT
python -m venv env
# Activate venv
# Windows:
.\env\Scripts\activate
# Mac/Linux:
source env/bin/activate


pip install -r requirements.txt


python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

