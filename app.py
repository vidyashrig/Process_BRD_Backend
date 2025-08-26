# app.py
from process_form.models import db
from process_form.routes import process_bp
from process_form import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)