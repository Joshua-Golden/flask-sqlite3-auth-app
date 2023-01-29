import os
import sqlite3

class Config:
    SECRET_KEY = os.environ.get('a407e11ecc0f751741fb542feaf26708')
    SQLALCHEMY_DATABASE_URI = "sqlite:///auth.db"
