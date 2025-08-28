from flask import (
    Blueprint,
    render_template,
)

from utils.request_monitor import request_monitor
from .home_utils import get_2025_weight_dict


home_bp = Blueprint("home", __name__)


@home_bp.route("/home", methods=["GET"])
def home():
    request_monitor.monitor()
    return render_template(
        "home/home.html",
    )


@home_bp.route("/weight", methods=["GET"])
@home_bp.route("/weight/<month>", methods=["GET"])
def weight(month=None):
    request_monitor.monitor()
    # Use a relative path for the image
    if month:
        path_s = f"images/weight_{month.lower()}_2025_s.png"
        path_l = f"images/weight_{month.lower()}_2025_l.png"
    else:
        path_s = "images/weight_july_2025_s.png"
        path_l = "images/weight_july_2025_l.png"
    
    title = " ".join(path_s.split("/")[-1].split("_")[:-1]).title()

    months2025 = get_2025_weight_dict()

    return render_template(
        "home/weight.html",
        title=title,
        path_s=path_s,
        path_l=path_l,
        months2025=months2025,
    )
