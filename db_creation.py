from typing import Tuple

import sqlalchemy

# для создания коннекта с базой данных нужно создать **движок**
from sqlalchemy import Column, Integer, String, ForeignKey, Text, inspect, UniqueConstraint, Identity, Sequence
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()
person_id=0
drink_id = 0
def people_increment():
    global person_id
    person_id+=1
    return person_id
def coffee_increment():
    global drink_id
    drink_id+=1
    return drink_id


class PeopleCoffee(Base):
    __tablename__ = 'people_coffee'
    __table_args__ =  (UniqueConstraint('people_id', 'coffee_id', name='personal_coffee'),)
    people_coffee_id_seq = Sequence('people_coffee_id_seq', metadata=Base.metadata)
    id = Column(Integer, people_coffee_id_seq, server_default=people_coffee_id_seq.next_value(), primary_key=True)
    people_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    coffee_id = Column(Integer, ForeignKey('coffee.id'), nullable=False)



class People(Base):
    __tablename__ = 'people'
    __table_args__ = (UniqueConstraint('first_name', 'last_name', name='person'),)
    people_id_seq = Sequence('people_id_seq', metadata=Base.metadata)
    id = Column(Integer,people_id_seq,server_default=people_id_seq.next_value(), primary_key=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    coffee = relationship('PeopleCoffee', backref='people')


class Coffee(Base):
    __tablename__ = 'coffee'
    __table_args__ = (UniqueConstraint('coffee_name', name='coffee_unique'),)
    coffee_id_seq = Sequence('coffee_id_seq', metadata=Base.metadata)
    id = Column(Integer,coffee_id_seq,server_default=coffee_id_seq.next_value(), primary_key=True)
    coffee_name = Column(Text, nullable=False)
    people = relationship('PeopleCoffee', backref='coffee')


def main(login: str, password: str) -> Engine:
    engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{login}:{password}@localhost:5432/',
                                      isolation_level='AUTOCOMMIT', echo=True)
    with engine.connect() as connection:
        if inspect(engine).has_table(engine, 'romturino_db'):
            connection.execute('CREATE DATABASE romturino_db')  # создание базы данных, если ее нет
        Base.metadata.create_all(connection)  # декларирование таблиц

    return engine

