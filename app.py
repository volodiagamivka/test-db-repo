from flask import Flask
from __init__ import create_app
from my_project.auth.route.user_route import user_bp
from my_project.auth.route.category_route import category_bp
from my_project.auth.route.property_route import property_bp
from my_project.auth.route.property_categories_route import property_category_bp

app = create_app()

app.register_blueprint(user_bp)
app.register_blueprint(category_bp)
app.register_blueprint(property_bp)
app.register_blueprint(property_category_bp)


if __name__ == '__main__':
    app.run(debug=True)
