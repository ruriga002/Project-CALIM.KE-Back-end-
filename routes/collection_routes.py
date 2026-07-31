from flask import Blueprint

from middleware.auth import admin_required

from controllers.collection_controller import (
    get_collections,
    get_collection,
    create_collection,
    update_collection,
    delete_collection
)

collection_bp = Blueprint(
    "collections",
    __name__
)


# ==========================
# Public Routes
# ==========================

@collection_bp.route("/", methods=["GET"])
def all_collections():
    return get_collections()


@collection_bp.route("/<int:collection_id>", methods=["GET"])
def single_collection(collection_id):
    return get_collection(collection_id)


# ==========================
# Admin Routes
# ==========================

@collection_bp.route("/", methods=["POST"])
@admin_required
def add_collection():
    return create_collection()


@collection_bp.route("/<int:collection_id>", methods=["PUT"])
@admin_required
def edit_collection(collection_id):
    return update_collection(collection_id)


@collection_bp.route("/<int:collection_id>", methods=["DELETE"])
@admin_required
def remove_collection(collection_id):
    return delete_collection(collection_id)