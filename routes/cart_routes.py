from flask import Blueprint

from middleware.auth import jwt_required_custom

from controllers.cart_controller import (
    get_cart,
    add_to_cart,
    update_cart,
    delete_cart_item
)

cart_bp = Blueprint(
    "cart",
    __name__
)


@cart_bp.route("/", methods=["GET"])
@jwt_required_custom
def view_cart():
    return get_cart()


@cart_bp.route("/", methods=["POST"])
@jwt_required_custom
def add_item():
    return add_to_cart()


@cart_bp.route("/<int:cart_id>", methods=["PUT"])
@jwt_required_custom
def edit_item(cart_id):
    return update_cart(cart_id)


@cart_bp.route("/<int:cart_id>", methods=["DELETE"])
@jwt_required_custom
def remove_item(cart_id):
    return delete_cart_item(cart_id)