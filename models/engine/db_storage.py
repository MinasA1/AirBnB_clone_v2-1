#!/usr/bin/python3
"""Database storage engine using SQLAlchemy with a mysql+mysqldb database
connection.
"""

import os
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
name2class = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}
names = {'Amenity': 'amenities', 'City': 'cities', 'Place': 'places',
         'Review': 'reviews', 'State': 'states', 'User': 'users'}


class DBStorage:
    __engine = None
    __session = None
    __count = {'amenities': 0, 'cities': 0, 'places': 0,
               'reviews': 0, 'states': 0, 'users': 0}

    def __init__(self):
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, database))
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        if not self.__session:
            self.reload()
        objects = {}
        if type(cls) == str:
            cls = name2class.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in name2class.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def reload(self):
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        name = obj.__class__.__name__
        self.__count[names[name]] += 1
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if not self.__session:
            self.reload()
        if obj:
            name = obj.__class__.__name__
            self.__count[names[name]] -= 1
            self.__session.delete(obj)

    def close(self):
        """Dispose of current session if active"""
        self.__session.remove()

    def get(self, cls, id):
        """returns the object mathing cls and id"""
        if cls is None or id is None:
            return None
        if type(cls) == str:
            cls = name2class.get(cls, None)
        objects = self.all(cls)
        key = cls.__name__ + '.' + id
        return objects.get(key, None)

    def count(self, cls=None):
        """returns count of all objects in storage"""
        if cls:
            return len(self.all(name2class[cls]))
        else:
            return len(self.all())
