from flask import request, jsonify
from my_project.auth.service.Users import UserService

user_service = UserService()

# Отримати всіх користувачів
def get_all_users():
    users = user_service.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200

# Отримати користувача за ID
def get_user_by_id(user_id):
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'message': 'User not found'}), 404

# Створити нового користувача
def create_user():
    data = request.json
    new_user = user_service.create_user(data)
    return jsonify(new_user.to_dict()), 201

# Оновити користувача за ID
def update_user(user_id):
    data = request.json
    updated_user = user_service.update_user(user_id, data)
    if updated_user:
        return jsonify(updated_user.to_dict()), 200
    return jsonify({'message': 'User not found'}), 404

# Видалити користувача за ID
def delete_user(user_id):
    success = user_service.delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

# Отримати всіх користувачів з деталями про їх властивості
def get_users_with_properties():
    users_with_properties = user_service.get_users_with_properties()
    return jsonify(users_with_properties), 200
