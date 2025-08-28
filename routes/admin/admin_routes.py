from flask import (
    Blueprint,
    flash,
    render_template,
    redirect,
    url_for,
)

from app import cache
from utils.upstash import upstash
from utils.request_monitor import request_monitor
from .admin_utils import WeightForm


admin_bp = Blueprint("admin", __name__)
CACHE_DURATION = 3600


@admin_bp.route("/admin/requests", methods=["GET"])
@cache.cached(timeout=CACHE_DURATION)
def requests():
    """Display requests"""
    tracking_data = request_monitor.get_request_data()
    return render_template(
        "admin/requests.html",
        title="Requests",
        tracking_data=tracking_data,
    )


@admin_bp.route("/admin/weight", methods=["GET", "POST"])
def weight():
    """Displays weight form."""
    weight_form = WeightForm()

    if weight_form.validate_on_submit():
        if upstash.check_weight_data(weight_form.date.data):
            flash("Weight data already exists")
        else:
            upstash.save_weight_data(weight_form.date.data, weight_form.weight.data)
            flash(f"Saved {weight_form.weight.data} on {weight_form.date.data}")
        
        return redirect(url_for("admin.weight"))
    
    return render_template(
        "admin/weight.html",
        title="Weight",
        weight_form=weight_form,
    )
