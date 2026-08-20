from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(10), unique=True, nullable=False) # e.g. s001, ib001, ob001
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # Roles: 'supervisor', 'inbound_emp', 'outbound_emp'
    role = db.Column(db.String(20), nullable=False)
    
    is_account_active = db.Column(db.Boolean, default=True, nullable=False)
    
    @property
    def is_active(self):
        return self.is_account_active

    transactions = db.relationship('Transaction', backref='requester', lazy=True)

    def __repr__(self):
        return f"<User {self.staff_id} ({self.name}) - Role: {self.role}>"


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    current_stock = db.Column(db.Integer, default=0)
    min_threshold = db.Column(db.Integer, default=5)
    
    transactions = db.relationship('Transaction', backref='product', lazy=True)

    def __repr__(self):
        return f"<Product {self.name} (Stock: {self.current_stock})>"


class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    txn_type = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), default='PENDING', nullable=False)
    rejection_reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    def __repr__(self):
        return f"<Transaction #{self.id} {self.txn_type} - {self.status}>"
