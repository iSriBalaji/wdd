# copied from fastapi sqlalchemy documentations//
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# all the models we see here are actual tables and their relationships defined in the database and tables

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    post = Column(String)
    user_id = Column(Integer, ForeignKey('user.id', )) # here user is the __tablename__ which is user

    creator = relationship('User', back_populates='post') # identified the post relationship in the User model or vice versa to establish a relationship

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key= True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    post = relationship('Post', back_populates='creator') # this line is just defining the relationships not the keys