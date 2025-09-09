import os

# Vercel Python Serverless Function entry for Flask via vercel-wsgi
from vercel_wsgi import handle

# Import the Flask app instance
from app import app as flask_app


def handler(event, context):
    # Delegate to vercel-wsgi adapter
    return handle(flask_app, event, context)

