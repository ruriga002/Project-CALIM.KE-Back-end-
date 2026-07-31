from database.db import db


class Collection(db.Model):

    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)

    description = db.Column(db.Text)

    image = db.Column(db.String(255))

    featured = db.Column(db.Boolean, default=False)

    # One Collection -> Many Products
    products = db.relationship(
        "Product",
        backref="collection",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "featured": self.featured
        }