from flask import Blueprint

from middleware.auth import jwt_required_custom, admin_required

from controllers.product_controller import (
    get_products,
    get_product,
    create_product,
    update_product,
    delete_product
)

product_bp = Blueprint(
    "products",
    __name__
)


# ==========================
# Public Routes
# ==========================

@product_bp.route("/", methods=["GET"])
def all_products():
    return get_products()


@product_bp.route("/<int:product_id>", methods=["GET"])
def single_product(product_id):
    return get_product(product_id)


# ==========================
# Admin Protected Routes
# ==========================

@product_bp.route("/", methods=["POST"])
@admin_required
def add_product():
    return create_product()


@product_bp.route("/<int:product_id>", methods=["PUT"])
@admin_required
def edit_product(product_id):
    return update_product(product_id)


@product_bp.route("/<int:product_id>", methods=["DELETE"])
@admin_required
def remove_product(product_id):
    return delete_product(product_id)