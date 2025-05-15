from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class MyClient(db.Model):
    __tablename__ = 'my_client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    is_project = db.Column(db.String(30), nullable=False, default='0')
    self_capture = db.Column(db.String(1), nullable=False, default='1')
    client_prefix = db.Column(db.String(4), nullable=False)
    client_logo = db.Column(db.String(255), nullable=False, default='no-image.jpg')
    address = db.Column(db.Text, default=None)
    phone_number = db.Column(db.String(50), default=None)
    city = db.Column(db.String(50), default=None)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), default=None)
    updated_at = db.Column(db.DateTime(timezone=True), default=None)
    deleted_at = db.Column(db.DateTime(timezone=True), default=None)
    
    def to_dict(self):
        return {
            "id" : self.id,
            "name": self.name,
            "slug": self.slug,
            "is_project" : self.is_project,
            "self_capture": self.self_capture,
            "client_prefix": self.client_prefix,
            "client_logo": self.client_logo,
            "address": self.address,
            "phone_number": self.phone_number,
            "city": self.city,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None      
        }
    