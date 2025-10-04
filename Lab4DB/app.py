from Lab4DB.app import create_app
from flask_restx import Api

app = create_app()

api = Api(app,
          title="IT Service Request Manager API",
          version="1.0",
          description="Documentation REST API for IT Service Request Manager",
          doc="/docs")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
