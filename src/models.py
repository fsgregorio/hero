"""
Database models for representing social media account data.

This module defines the SQLAlchemy ORM models for accounts, categories,
and historical subscriber data, establishing relationships between them.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Account(Base):
    """
    Represents a social media account.
    
    Attributes:
        account_id (str): Unique identifier for the account.
        categories (relationship): Relationship to AccountCategory.
        history (relationship): Relationship to Historical records.
    """
    __tablename__ = "accounts"
    account_id = Column(String, primary_key=True, index=True)
    categories = relationship("AccountCategory", back_populates="account")
    history = relationship("Historical", back_populates="account")

class Category(Base):
    """
    Represents a category for social media accounts.
    
    Attributes:
        id (int): Unique identifier for the category.
        name (str): Name of the category.
    """
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class AccountCategory(Base):
    """
    Association table between accounts and categories.
    
    Attributes:
        id (int): Unique identifier for the relationship.
        account_id (str): Foreign key referencing the Account.
        category_id (int): Foreign key referencing the Category.
    """
    __tablename__ = "account_and_categories"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.account_id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    account = relationship("Account", back_populates="categories")
    category = relationship("Category")

class Historical(Base):
    """
    Represents historical follower data for an account.
    
    Attributes:
        id (int): Unique identifier for the historical record.
        account_id (str): Foreign key referencing the Account.
        subscriber_count (int): Number of subscribers at a given point in time.
        date (datetime): Date of the recorded subscriber count.
    """
    __tablename__ = "historical"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.account_id"))
    subscriber_count = Column(Integer, index=True)
    date = Column(DateTime, index=True)
    account = relationship("Account", back_populates="history")