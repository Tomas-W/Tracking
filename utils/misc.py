import os

from flask import session, redirect, url_for, flash, request
from functools import wraps
from PIL import Image

from utils.config import CFG


def login_required(f):
    """Redirects to login page if user is not logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("You need to be logged in to access this page.")
            return redirect(url_for(CFG.redirect.landing, next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def img_to_webp():
    img_dir = os.path.join("static", "images")
    for filename in os.listdir(img_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(img_dir, filename)
            with Image.open(img_path) as img:
                webp_path = os.path.splitext(img_path)[0] + '.webp'
                img.save(webp_path, 'WEBP', quality=85)
