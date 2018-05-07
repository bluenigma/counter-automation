from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_init import Unit, Client, Base

engine = create_engine('sqlite:///counter_autom.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class unit():
    def __init__(self,sn,model,black_count,color_count,client_id):
        self.sn = sn
        self.model = model
        self.black_count = black_count
        self.color_count = color_count
        self.client_id = client_id
    def __del__(self):
        print('Unit removed.')
    def __repr__(self):
        return f'Unit {self.sn}\nModel {self.model}'
    def modify(self,property_to_change,new_value):
        pass
    def commit_to_db(self):
        session.add(self)
        session.commit()



if __name__ == '__main__':
    pass
