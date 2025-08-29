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
from utils.logger import logger
from utils.config import CFG


landing_bp = Blueprint("landing", __name__)


@landing_bp.route(CFG.route.landing, methods=["GET", "POST"])
def landing():
    """Displays login form."""
    request_monitor.monitor()
    
    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():

            username = login_form.username.data
            password = login_form.password.data
            user = upstash.get_user(username)
            logger.info(f"Trying to login: {username=} {password=} {user=}")

            if user is not None and user == password:
                session["username"] = username
                next_url = request.args.get("next")
                logger.info(f"Logged in: {username=}")
                return redirect(next_url or url_for(CFG.redirect.home))
            else:
                flash("Incorrect credentials")
                logger.info(f"Incorrect credentials: {username=}")
        
        else:
            session["form_errors"] = login_form.errors
    
    form_errors = session.pop("form_errors", None)
    return render_template(
        CFG.template.landing,
        login_form=login_form,
        form_errors=form_errors
    )