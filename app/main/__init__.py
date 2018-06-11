from flask import Blueprint
main = Blueprint('main', __name__)
from app.main import starter_views
from app.main.VR import *
