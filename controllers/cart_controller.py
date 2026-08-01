from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from database.db import db

from models.cart import Cart
from models.product import Product


# GET /api/cart
def get_cart():

    user_id = get_jwt_identity()

    cart = Cart.query.filter_by(user_id=user_id).all()

    return jsonify([item.to_dict() for item in cart])


# POST /api/cart
def add_to_cart():

    data = request.get_json() or {}

    user_id = get_jwt_identity()

    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        return jsonify({
            "message": "product_id is required."
        }), 400

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found."
        }), 404

    cart_item = Cart.query.filter_by(
        user_id=user_id,
        product_id=product.id
    ).first()

    if cart_item:
        cart_item.quantity += data.get("quantity", 1)
    else:
        cart_item = Cart(
            user_id=user_id,
            product_id=product.id,
            quantity=data.get("quantity", 1)
        )
        db.session.add(cart_item)

    db.session.commit()

    return jsonify({
        "message": "Added to cart.",
        "cart": cart_item.to_dict()
    }), 201


# PUT /api/cart/<id>
def update_cart(cart_id):

    item = Cart.query.get(cart_id)

    if not item:
        return jsonify({
            "message": "Cart item not found."
        }), 404

    data = request.get_json() or {}

    item.quantity = data.get("quantity", item.quantity)

    db.session.commit()

    return jsonify({
        "message": "Cart updated.",
        "cart": item.to_dict()
    })


# DELETE /api/cart/<id>
def delete_cart_item(cart_id):

    item = Cart.query.get(cart_id)

    if not item:
        return jsonify({
            "message": "Cart item not found."
        }), 404

    db.session.delete(item)

    db.session.commit()

    return jsonify({
        "message": "Item removed from cart."
    })