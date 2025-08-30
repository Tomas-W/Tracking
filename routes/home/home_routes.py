from flask import (
    Blueprint,
    render_template,
)
from typing import Final

from utils.request_monitor import request_monitor
from .home_utils import (
    get_2025_calories_dict,
    get_2025_weight_dict,
    get_calories_image_paths,
    get_weight_image_paths,
    get_image_title
)
from utils.misc import login_required
from utils.config import CFG
from utils.logger import logger


home_bp = Blueprint("home", __name__)
CACHE_DURATION: Final = 3600


@home_bp.route(CFG.route.home, methods=["GET"])
@login_required
def home():
    """Displays empty page."""
    return render_template(
        CFG.template.home,
    )


@home_bp.route(CFG.route.weight, methods=["GET"])
@home_bp.route(f"{CFG.route.weight}/<month>", methods=["GET"])
@login_required
def weight(month=None):
    """Displays weight images and month selection."""
    request_monitor.monitor()

    path_s, path_l = get_weight_image_paths(month)
    title = get_image_title(path_s, month)
    months2025 = get_2025_weight_dict()
    url = CFG.redirect.weight

    return render_template(
        CFG.template.graph,
        title=title,
        path_s=path_s,
        path_l=path_l,
        months2025=months2025,
        current_month=month,
        url=url,
    )


@home_bp.route(CFG.route.calories, methods=["GET"])
@home_bp.route(f"{CFG.route.calories}/<month>", methods=["GET"])
@login_required
def calories(month=None):
    """Displays weight images and month selection."""
    request_monitor.monitor()

    path_s, path_l = get_calories_image_paths(month)
    title = get_image_title(path_s, month)
    months2025 = get_2025_calories_dict()
    url = CFG.redirect.calories

    return render_template(
        CFG.template.graph,
        title=title,
        path_s=path_s,
        path_l=path_l,
        months2025=months2025,
        current_month=month,
        url=url,
    )
