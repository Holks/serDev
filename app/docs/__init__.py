from flask import Blueprint
from config import docs_dir

#, static_url_path='/', static_folder=docs_dir
bp = Blueprint('docs', __name__ , static_url_path='/', static_folder=docs_dir)

from app.docs import routes
