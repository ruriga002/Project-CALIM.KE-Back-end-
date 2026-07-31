from flask import Blueprint

from middleware.auth import jwt_required_custom

from controllers.order_controller import (
    get_orders,
    get_order,
    create_order,
    update_order,
    delete_order
)

order_bp = Blueprint(
    "orders",
    __name__
)


@order_bp.get("/")
@jwt_required_custom
def orders():
    return get_orders()


@order_bp.get("/<int:order_id>")
@jwt_required_custom
def order(order_id):
    return get_order(order_id)


@order_bp.post("/")
@jwt_required_custom
def create():
    return create_order()


@order_bp.put("/<int:order_id>")
@jwt_required_custom
def update(order_id):
    return update_order(order_id)


@order_bp.delete("/<int:order_id>")
@jwt_required_custom
def delete(order_id):
    return delete_order(order_id)