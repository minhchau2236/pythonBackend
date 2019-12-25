from flask import current_app
from datetime import datetime, timedelta
from app import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    is_deleted = db.Column(db.Boolean)
    created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified_time = db.Column(db.DateTime, index=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    latest_modified_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id')),
    name = db.Column(db.String(250)),
    description = db.Column(db.Text(1000))

    def __repr__(self):
        return '<Category {}>'.format(self.name)