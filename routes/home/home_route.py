from flask import (
    Blueprint,
    render_template,
)

from utils.request_monitor import request_monitor


home_bp = Blueprint("home", __name__)


@home_bp.route("/home", methods=["GET"])
def home():
    request_monitor.monitor()
    
    return render_template(
        "home/home.html",
        title="Home"
    )
