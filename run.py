import argparse
import os

from app import get_app

app = get_app()
application = app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Flask application")
    parser.add_argument("--local", action="store_true", default=False, help="Run the application in debug mode")
    args = parser.parse_args()
    debug = args.local

    port = int(os.getenv("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )
