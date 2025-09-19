from flask import Blueprint, render_template
from routes import routes_helpers as rs

hist_bp = Blueprint('hist_bp', __name__)

@hist_bp.route("/history")
def history():
    return rs.history()