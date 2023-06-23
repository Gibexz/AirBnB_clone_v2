#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable = False)
    cities = relationship("City", cascade='all, delete', backref='state')

    @property
    def cities(self):
        list_cites=[]
        for key, value in self.__obecjs.items():
            if value.__class__.__name__ == 'City' and self.state_id == self.id:
                list_cites.append(value)
        return list_cites
