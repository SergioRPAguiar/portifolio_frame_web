import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'development-key'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}