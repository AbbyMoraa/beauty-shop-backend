import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import application
app = application.app

# Create tables if they don't exist (safe to run multiple times)
try:
    with app.app_context():
        from models import db
        db.create_all()
except Exception as e:
    print(f"Warning: Could not create tables: {e}")

if __name__ == "__main__":
    app.run()
