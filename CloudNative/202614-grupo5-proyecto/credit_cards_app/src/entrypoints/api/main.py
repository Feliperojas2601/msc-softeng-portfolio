from assembly import create_app
from config import settings

app = create_app()


if __name__ == "__main__":
    from adapters.database.session import init_models

    init_models()
    app.run(host="0.0.0.0", port=settings.app_port, threaded=False)
