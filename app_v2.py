from flask import Flask

app = Flask(__name__)
app.secret_key = "edumate123"

# Import Blueprints
from auth import auth_bp
from admin import admin_bp
from teacher import teacher_bp
from student import student_bp
from parent import parent_bp

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(student_bp)
app.register_blueprint(parent_bp)

print("\n========== REGISTERED ROUTES ==========")

for rule in app.url_map.iter_rules():
    print(rule)

print("=======================================\n")

if __name__ == "__main__":
    app.run(debug=True)