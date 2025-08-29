from flask import (
    Blueprint,
    flash,
    render_template,
    redirect,
    url_for,
)

from utils.upstash import upstash
from utils.request_monitor import request_monitor
from .admin_utils import AddUserForm
from utils.misc import login_required


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/requests", methods=["GET"])
@login_required
def requests():
    """Display requests"""
    tracking_data = request_monitor.get_request_data()
    if not tracking_data:
        tracking_data = []
    
    print(f"tracking_data: {len(tracking_data)}")
    print(f"session: ")
    print(f"session: ")

    return render_template(
        "admin/requests.html",
        title="Requests",
        tracking_data=tracking_data,
    )


@admin_bp.route("/admin/add-user", methods=["GET", "POST"])
@login_required
def add_user():
    """Displays add user form."""
    add_user_form = AddUserForm()
    print(f"add_user_form: ")

    if add_user_form.validate_on_submit():
        if upstash.check_user_data(add_user_form.username.data):
            flash("User already exists")
        else:
            upstash.save_user_data(add_user_form.username.data, add_user_form.password.data)
            flash(f"Saved {add_user_form.username.data} on {add_user_form.password.data}")
        
        return redirect(url_for("admin.add_user"))
    
    return render_template(
        "admin/add_user.html",
        title="Add User",
        add_user_form=add_user_form,
    )
