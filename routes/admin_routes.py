from flask import Blueprint

from controllers.admin_controller import (
    dashboard,
    get_customers,
    delete_customer,
    get_products_admin,
    get_orders,
    update_order,
    inventory
)

admin_bp = Blueprint("admin", __name__)


# ==========================
# Dashboard
# ==========================
admin_bp.route(
    "/dashboard",
    methods=["GET"]
)(dashboard)


# ==========================
# Customers
# ==========================
admin_bp.route(
    "/customers",
    methods=["GET"]
)(get_customers)

admin_bp.route(
    "/customers/<int:customer_id>",
    methods=["DELETE"]
)(delete_customer)


# ==========================
# Products
# ==========================
admin_bp.route(
    "/products",
    methods=["GET"]
)(get_products_admin)


# ==========================
# Orders
# ==========================
admin_bp.route(
    "/orders",
    methods=["GET"]
)(get_orders)

admin_bp.route(
    "/orders/<int:order_id>",
    methods=["PATCH"]
)(update_order)


# ==========================
# Inventory
# ==========================
admin_bp.route(
    "/inventory",
    methods=["GET"]
)(inventory)