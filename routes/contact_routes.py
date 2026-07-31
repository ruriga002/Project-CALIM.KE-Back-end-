from flask import Blueprint

from middleware.auth import admin_required

from controllers.contact_controller import (
    submit_contact,
    get_contacts,
    delete_contact
)

contact_bp = Blueprint(
    "contact",
    __name__
)


# Public
@contact_bp.route("/", methods=["POST"])
def send_message():
    return submit_contact()


# Admin
@contact_bp.route("/", methods=["GET"])
@admin_required
def contacts():
    return get_contacts()


@contact_bp.route("/<int:contact_id>", methods=["DELETE"])
@admin_required
def remove_contact(contact_id):
    return delete_contact(contact_id)