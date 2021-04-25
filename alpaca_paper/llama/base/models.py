from .. import db
from datetime import datetime


class BaseDBModel():
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    soft_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Deprecated, use serializers instead
    def json(self):
        return {
            'id': self.id
        }

    def get_public_fields():
        return (
            'id', 'created_at', 'updated_at'
        )

    def delete(self):
        self.soft_deleted = True
        db.session.commit()

    def save_to_db(self):
        now = datetime.now()
        if not self.id:
            self.created_at = now
        
        self.updated_at = now
        db.session.add(self)
        db.session.commit()
