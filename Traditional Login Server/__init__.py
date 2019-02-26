from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load configs from a file.
app.config.from_object('config')

# Disable browser caching. It causes showing the same QR code even if it is changed.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(app)

from app import views, models
