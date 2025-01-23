#!/usr/bin/python3
"""This is the DBStorage class for AirBnB"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class DBStorage:
    """This is the DBStorage class for AirBnB"""

    engine = None
    session = None

    def __init__(self):
        
        username = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        dtb_name = getenv('HBNB_MYSQL_DB')

        db_url = "mysql+mysqldb://{}:{}@{}/{}".format(username, password, host, dtb_name)

        self.engine = create_engine(db_url, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.engine)


    def all(self, cls=None):
        """query on the current database session"""
        objs_list = []

        if cls: 
            if isinstance(cls, str):
                try:
                    cls = globals()[cls]  
                except KeyError:
                    pass   

            if issubclass(cls, BaseModel):
                objs_list = self.session.query(cls).all()

        else:
            for subclass in Base.__subclasses__():
                objs_list.extend(self.session.query(subclass).all())
        obj_dict = {}
        for obj in objs_list:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            obj_dict[key] = obj
            try:
                del obj.sa_instance_state
                obj_dict[key] = obj
            except Exception:
                pass
        return obj_dict
    
    def new(self, obj):
        """add the object to the current database session"""
        self.session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.session.commit()   

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.engine)
        session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.session = Session()
