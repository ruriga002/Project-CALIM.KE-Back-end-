from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from database.db import db

from models.order import Order
from models.order_item import OrderItem
from models.product import Product


def get_orders():

    user_id = get_jwt_identity()

    orders = Order.query.filter_by(user_id=user_id).all()

    return jsonify([order.to_dict() for order in orders])


def get_order(order_id):

    user_id = get_jwt_identity()

    order = Order.query.filter_by(
        id=order_id,
        user_id=user_id
    ).first()

    if not order:
        return jsonify({
            "message": "Order not found."
        }), 404

    return jsonify(order.to_dict())


def create_order():

    data = request.get_json()

    user_id = get_jwt_identity()

    order = Order(
        user_id=user_id,
        status="Pending",
        total_price=0,
        shipping_address=data["shipping_address"]
    )

    db.session.add(order)
    db.session.flush()

    total = 0

    for item in data["items"]:

        product = Product.query.get(item["product_id"])

        if not product:
            continue

        subtotal = product.price * item["quantity"]

        total += subtotal

        db.session.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item["quantity"],
                price=product.price
            )
        )

    order.total_price = total

    db.session.commit()

    return jsonify({
        "message": "Order placed successfully.",
        "order": order.to_dict()
    }), 201


def update_order(order_id):

    user_id = get_jwt_identity()

    order = Order.query.filter_by(
        id=order_id,
        user_id=user_id
    ).first()

    if not order:
        return jsonify({"message": "Order not found."}), 404

    data = request.get_json()

    order.status = data.get("status", order.status)

    order.shipping_address = data.get(
        "shipping_address",
        order.shipping_address
    )

    db.session.commit()

    return jsonify(order.to_dict())


def delete_order(order_id):

    user_id = get_jwt_identity()

    order = Order.query.filter_by(
        id=order_id,
        user_id=user_id
    ).first()

    if not order:
        return jsonify({"message": "Order not found."}), 404

    db.session.delete(order)

    db.session.commit()

    return jsonify({
        "message": "Order deleted successfully."
    })