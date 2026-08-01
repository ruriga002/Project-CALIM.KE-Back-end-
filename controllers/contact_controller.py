from flask import request, jsonify

from database.db import db
from models.contact import Contact


def submit_contact():

    data = request.get_json() or {}

    required = [
        "name",
        "email",
        "subject",
        "message"
    ]

    for field in required:

        if not data.get(field):
            return jsonify({
                "message": f"{field} is required."
            }), 400

    contact = Contact(
        name=data["name"],
        email=data["email"],
        subject=data["subject"],
        message=data["message"]
    )

    db.session.add(contact)
    db.session.commit()

    return jsonify({
        "message": "Message sent successfully.",
        "contact": contact.to_dict()
    }), 201


def get_contacts():

    contacts = Contact.query.order_by(
        Contact.created_at.desc()
    ).all()

    return jsonify([
        contact.to_dict()
        for contact in contacts
    ])


def delete_contact(contact_id):

    contact = Contact.query.get(contact_id)

    if not contact:
        return jsonify({
            "message": "Contact not found."
        }), 404

    db.session.delete(contact)

    db.session.commit()

    return jsonify({
        "message": "Contact deleted successfully."
    })