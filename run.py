import os

from app import get_app

from routes.landing.landing_route import landing_bp
from routes.home.home_route import home_bp
from routes.admin.admin_routes import admin_bp

app = get_app()
application = app

app.register_blueprint(landing_bp)
app.register_blueprint(home_bp)
app.register_blueprint(admin_bp)


@app.route("/health")
def railway_healthcheck():
    return "OK", 200


if __name__ == "__main__":
    # debug = os.getenv("DEBUG", "True")
    port = int(os.getenv("PORT", 8080))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
    