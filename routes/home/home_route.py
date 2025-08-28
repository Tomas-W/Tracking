from flask import (
    Blueprint,
    render_template,
)

from utils.request_monitor import request_monitor


home_bp = Blueprint("home", __name__)


@home_bp.route("/home", methods=["GET"])
def home():
    request_monitor.monitor()
    # Use a relative path for the image
    graph_path = "images/weight_july_2005_s.png"
    path_s = "images/weight_july_2005_s.png"
    path_l = "images/weight_july_2005_l.png"
    title = " ".join(graph_path.split("/")[-1].split("_")[:-1]).title()

    return render_template(
        "home.html",
        title=title,
        path_s=path_s,
        path_l=path_l,
    )
