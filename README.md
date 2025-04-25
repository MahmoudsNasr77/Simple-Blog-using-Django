# 📝 Simple Blog using Django

A basic blogging platform built with Django. This project allows users to create, read, update, and delete blog posts with a clean and simple UI.

## 🚀 Features

- 🧑‍💻 User authentication (Login, Logout)
- 📝 Create, Read, Update, Delete (CRUD) blog posts
- 🔒 Authorization: only the author can edit/delete their posts
- 📄 Post detail view with formatted content
- 📆 Automatic timestamps for posts
- 🧼 Clean UI using Bootstrap

## 🛠 Tech Stack

- **Framework:** Django
- **Language:** Python
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default)
- **Templates Engine:** Django Templates

## 📦 Installation & Setup

Follow the steps below to run the project locally:

### 1. Clone the repository

```bash
git clone https://github.com/MahmoudsNasr77/Simple-Blog-using-Django.git
cd Simple-Blog-using-Django
```
### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Run Migrations
```
bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Create Superuser (for admin access)
```bash
python manage.py createsuperuser
```
### 7. Run the Development Server
```bash
python manage.py runserver
Visit http://127.0.0.1:8000/ in your browse
```
