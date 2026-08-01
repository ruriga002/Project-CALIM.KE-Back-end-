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

    data = request.get_json() or {}

    user_id = get_jwt_identity()

    shipping_address = data.get("shipping_address")
    items = data.get("items")

    if not shipping_address or not isinstance(items, list) or len(items) == 0:
        return jsonify({
            "message": "Shipping address and at least one item are required."
        }), 400

    order = Order(
        user_id=user_id,
        status="Pending",
        total_price=0,
        shipping_address=shipping_address
    )

    db.session.add(order)
    db.session.flush()

    total = 0

    for item in items:
        product_id = item.get("product_id")
        quantity = item.get("quantity", 1)

        if not product_id or quantity <= 0:
            continue

        product = Product.query.get(product_id)

        if not product:
            continue

        subtotal = product.price * quantity

        total += subtotal

        db.session.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                price=product.price
            )
        )

    order.total_price = total

    if len(order.items) == 0:
        db.session.rollback()
        return jsonify({
            "message": "Order must contain at least one valid product item."
        }), 400

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

    data = request.get_json() or {}

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