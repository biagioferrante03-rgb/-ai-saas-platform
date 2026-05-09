from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from models import db, User
from auth import auth_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return redirect(url_for("auth.login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
