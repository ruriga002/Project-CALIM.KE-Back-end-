from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from database.db import db
from models.user import User
from models.product import Product
from models.order import Order
from models.collection import Collection


# -----------------------------
# Check Admin
# -----------------------------
def admin_required():

    claims = get_jwt()

    if claims.get("role") != "admin":
        return False

    return True


# -----------------------------
# Dashboard Statistics
# -----------------------------
@jwt_required()
def dashboard():

    if not admin_required():
        return jsonify({"message": "Admin access required."}), 403

    return jsonify({

        "users": User.query.count(),

        "products": Product.query.count(),

        "orders": Order.query.count(),

        "collections": Collection.query.count()

    })


# -----------------------------
# Customers
# -----------------------------
@jwt_required()
def get_customers():

    if not admin_required():
        return jsonify({"message": "Admin access required."}), 403

    customers = User.query.all()

    return jsonify({

        "customers": [

            customer.to_dict()

            for customer in customers

        ]

    })


# -----------------------------
# Delete Customer
# -----------------------------
@jwt_required()
def delete_customer(customer_id):

    if not admin_required():
        return jsonify({"message": "Admin access required."}), 403

    customer = User.query.get(customer_id)

    if not customer:
        return jsonify({
            "message": "Customer not found."
        }), 404

    if customer.role == "admin":
        return jsonify({
            "message": "Cannot delete another admin."
        }), 403

    db.session.delete(customer)

    db.session.commit()

    return jsonify({
        "message": "Customer deleted successfully."
    })


# -----------------------------
# Admin Products
# -----------------------------
@jwt_required()
def get_products_admin():

    if not admin_required():
        return jsonify({"message": "Admin access required."}), 403

    products = Product.query.all()

    return jsonify({

        "products": [

            product.to_dict()

            for product in products

        ]

    })


# -----------------------------
# Orders
# -----------------------------
@jwt_required()
def get_orders():

    if not admin_required():
        return jsonify({"message": "Admin access required."}), 403

    orders = Order.query.all()

    return jsonify({

        "orders": [

            order.to_dict()

            for order in orders

        ]

    })


# -----------------------------
# Update Order Status
# -----------------------------
@jwt_required()
def update_order(order_id):

    if not admin_required():
        return jsonify({"message": "Admin access required."}), 403

    order = Order.query.get(order_id)

    if not order:
        return jsonify({
            "message": "Order not found."
        }), 404

    data = request.get_json()

    order.status = data.get("status", order.status)

    db.session.commit()

    return jsonify({

        "message": "Order updated successfully.",

        "order": order.to_dict()

    })


# -----------------------------
# Inventory
# -----------------------------
@jwt_required()
def inventory():

    if not admin_required():
        return jsonify({"products": [

            product.to_dict()

            for product in Product.query.all()

        ]})

    products = Product.query.all()

    return jsonify({

        "products": [

            product.to_dict()

            for product in products

        ]

    })