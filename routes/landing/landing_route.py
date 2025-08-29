from flask import (
    Blueprint,
    render_template,
    session,
    request,
    flash,
    redirect,
    url_for,
)

from utils.upstash import upstash
from utils.request_monitor import request_monitor
from .landing_utils import LoginForm


landing_bp = Blueprint("landing", __name__)


@landing_bp.route("/", methods=["GET", "POST"])
def landing():
    request_monitor.monitor()
    
    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data
            user = upstash.get_user(username)
            if user is not None and user == password:
                session["username"] = username
                next_url = request.args.get("next")
                return redirect(next_url or url_for("home.home"))
            else:
                flash("Incorrect credentials")
        
        else:
            session["form_errors"] = login_form.errors
    
    form_errors = session.pop("form_errors", None)
    flash("Incorrect credentials")
    return render_template(
        "landing/landing.html",
        login_form=login_form,
        form_errors=form_errors
    )