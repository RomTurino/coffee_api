from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from api_classes import CoffeeAPI, PeopleAPI
from db_creation import main, Coffee, People, PeopleCoffee

# change this information if it isn't correct
POSTGRESQL_LOGIN = 'postgres'
POSTGRESQL_PASSWORD = '123456'

engine = main(POSTGRESQL_LOGIN, POSTGRESQL_PASSWORD)
Session = sessionmaker(bind=engine, autoflush=True)
session = Session()

app = FastAPI()


@app.post('/coffee/create')
async def coffee_create(coffee_api: CoffeeAPI):
    coffee_obj = Coffee(**coffee_api.dict())
    session.add(coffee_obj)
    session.flush()
    return coffee_api


@app.get('/coffee/all')
async def coffee_list():
    all_coffee = session.query(Coffee).all()
    return all_coffee


@app.get('/coffee/{coffee_id}')
async def about_coffee(coffee_id: int):
    result = {}
    coffee = session.query(Coffee).get(coffee_id)
    if coffee:
        result.update({'coffee': coffee})
    if result:
        people_who_loves_coffee = session.query(PeopleCoffee).filter(PeopleCoffee.coffee_id == coffee_id)
        people_list = []
        for item in people_who_loves_coffee:
            people = session.query(People).get(item.people_id)
            people_list.append(people)
        result.update({'person': people_list})

    return result


@app.post('/people/create')
async def new_person(person_api: PeopleAPI, coffee_api: CoffeeAPI):
    person = People(**person_api.dict())
    coffee = Coffee(**coffee_api.dict())
    person.first_name = person.first_name.capitalize()
    person.last_name = person.last_name.capitalize()
    coffee.coffee_name = coffee.coffee_name.lower()
    is_exists = session.query(Coffee).filter(Coffee.coffee_name == coffee.coffee_name).scalar()
    if not is_exists:
        session.add(coffee)
    else:
        coffee.id = is_exists.id
    session.add(person)
    session.flush()
    person_coffee = PeopleCoffee(people_id=person.id, coffee_id=coffee.id)
    session.add(person_coffee)
    return {'person': person, 'coffee': coffee}


@app.get('/people/all')
async def people_list():
    all_people = session.query(People).all()
    return all_people


@app.get('/people/{person_id}')
async def about_person(person_id: int):
    result = {}
    person = session.query(People).get(person_id)
    if person:
        result.update({'person': person})
    if result:
        coffee_id_list = session.query(PeopleCoffee).filter(PeopleCoffee.people_id == person_id)
        coffee_list = []
        for item in coffee_id_list:
            coffee = session.query(Coffee).get(item.coffee_id)
            coffee_list.append(coffee)
        result.update({'coffee': coffee_list})
    return {'id_list': result}
