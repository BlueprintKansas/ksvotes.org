from flask import Blueprint
main = Blueprint('main', __name__)
from app.main import starter_views
from app.main import error_pages
from app.main.VR import *
from app.main.AB import *
