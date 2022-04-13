import sqlalchemy

# для создания коннекта с базой данных нужно создать **движок**
from sqlalchemy import Column, Integer, String, ForeignKey, Text, inspect
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
Session = sessionmaker(bind=engine)


class PeopleCoffee(Base):
    __tablename__ = 'people_coffee'
    id = Column(Integer, primary_key=True)
    people_id = Column(Integer, ForeignKey('people.id'))
    coffee_id = Column(Integer, ForeignKey('coffee.id'))


class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    coffee = relationship('PeopleCoffee', backref='people')


class Coffee(Base):
    __tablename__ = 'coffee'
    id = Column(Integer, primary_key=True)
    coffee_name = Column(Text, nullable=False)
    people = relationship('PeopleCoffee', backref='coffee')


def main(login: str, password: str):
    engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{login}:{password}@localhost:5432/',
                                      isolation_level='AUTOCOMMIT', echo=True)
    with engine.connect() as connection:
        if inspect(engine).has_table(engine, 'romturino_db'):
            connection.execute('CREATE DATABASE romturino_db')  # создание базы данных, если ее нет
        Base.metadata.create_all(connection)  # декларирование таблиц
    return engine
