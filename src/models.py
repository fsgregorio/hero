from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Account(Base):
    """
    Represents a social media account.
    """
    __tablename__ = "accounts"
    account_id = Column(String, primary_key=True, index=True)
    categories = relationship("AccountCategory", back_populates="account")
    history = relationship("Historical", back_populates="account")

class Category(Base):
    """
    Represents a category for social media accounts.
    """
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class AccountCategory(Base):
    """
    Association table between accounts and categories.
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
    """
    __tablename__ = "historical"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.account_id"))
    subscriber_count = Column(Integer, index=True)
    date = Column(DateTime, index=True)
    account = relationship("Account", back_populates="history")
