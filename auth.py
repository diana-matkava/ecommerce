import functools
from flask import Blueprint, flush, render_template, request, session, url_for, redirect
from werkzeug.security import check_password_hash, generate_password_hasj
from flask_tutor.db import open_connection

bp = Blueprint('auth', __name__, url_prefix='/auth')