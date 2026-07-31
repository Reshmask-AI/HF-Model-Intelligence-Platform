from flask import Flask

from app.routes import api


def create_app():
    """
    Application factory.
    Creates and configures the Flask application.
    """

    app = Flask(__name__)

    # Register API routes
    app.register_blueprint(api)

    return app


# Create Flask application
app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
