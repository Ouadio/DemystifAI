# -*- coding: utf-8 -*-

from flowers_recogn import db, image_names



class Flower(db.Model):
    __tablename__ = "flowers"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return(f"The flower's name is : {self.name}")
    
    
def populate():
    for name in image_names.loc[:,'name'].values:
        flower = Flower(name=name)
        db.session.add(flower)
        db.session.commit()
        
    
def depopulate():
    all_flowers = Flower.query.all()
    for flower in all_flowers:
        db.session.delete(flower)
        db.session.commit()