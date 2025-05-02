from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint, Index

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # Prevent duplicate customers with the same name, email, and phone
    __table_args__ = (
        db.UniqueConstraint('name', 'email', 'phone', name='uq_customer_identity'),
        Index('idx_customer_id', 'id', postgresql_using='hash')
    )

    # Foreign key constraint between Customer and Order - all associated orders should be deleted if customer is deleted
    orders = db.relationship("Order", backref="Customer", cascade="all,delete-orphan")

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(
        db.Integer,
        db.ForeignKey('customer.id'),
        nullable=False
    )
    order_time = db.Column(db.DateTime, nullable=False)
    order_size = db.Column(db.Integer, nullable=False)
    sale_value = db.Column(db.Float, nullable=False)

    # Prevent duplicate orders
    __table_args__ = (
        db.UniqueConstraint('customer_id', 'order_time', name='uq_order_entry'),
        Index('idx_order_time_size_value', 'order_time', 'order_size', 'sale_value'),
        Index('idx_order_id', 'id', postgresql_using='hash')
    )
