import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        
        # using SQLAlchemy
        return cls.query.filter_by(username=username).first()
        #without SQLAlchemy
        '''connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE username=?"
        
        result = cursor.execute(query, (username,)) # parameters always have to be in the form of TUPLE! (username,)
        row = result.fetchone()
        if row: # = if row is not None:
            user = cls(*row)    # (row[0], row[1], row[2])
        else:
            user = None
        
        connection.close()
        return user
        '''
    
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        '''connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE id=?"
        
        result = cursor.execute(query, (_id,)) # parameters always have to be in the form of TUPLE! (username,)
        row = result.fetchone()
        if row: # = if row is not None:
            user = cls(*row)    # (row[0], row[1], row[2])
        else:
            user = None
        
        connection.close()
        return user
        '''