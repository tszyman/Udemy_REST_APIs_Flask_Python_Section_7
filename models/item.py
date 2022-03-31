from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
        
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
        
        
    def json(self):
        return {'name': self.name, 'price':self.price}

    @classmethod
    def find_by_name(cls, name):
        '''
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        
        # query = "SELECT * FROM items where name = ?"
        
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        
        # if row:
        #     return cls(*row) #argument upacking form cls(row[0], row[1]) # previously we've returned a dictionary: {'item': {'name': row[0], 'price':row[1]}}, now we return an Object of the class (cls) 
        '''     
        ## rewriting everything above to SQLAlchemy
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1
        
        # insert no longer needed
        '''def insert(self):
                connection = sqlite3.connect('data.db')
                cursor = connection.cursor()
            
                query = "INSERT INTO items VALUES (?,?)"
                cursor.execute(query, (self.name, self.price))
                
                connection.commit()
                connection.close()
            
            ## rewriting everything above to SQLAlchemy
                db.session.add(self) # adds an Object to a database
                db.session.commit()
        '''
    def save_to_db(self):
        #instead of insert and update
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
        # update no longer needed 
        '''
        def update(self):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
                        
            query = "UPDATE items SET price=? where name=?"
            cursor.execute(query, (self.price,self.name))
            
            connection.commit()
            connection.close()
        '''