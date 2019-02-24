"""Data acquisition server server Documentation
"""
from app.docs import bp
from config import docs_dir
from flask import send_from_directory

@bp.route('/', methods=['GET'])
@bp.route('/<path:path>', methods=['GET'])
def serve_sphinx_docs(path='index.html'):
    """Serve documentation files to client from predefined location

    Care must be taken to avoid security breaches
    """
    return send_from_directory(docs_dir, path)
