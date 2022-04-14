from pydantic import BaseModel, Field


class CoffeeAPI(BaseModel):
    coffee_name: str = Field(title='Название кофе')


class PeopleAPI(BaseModel):
    first_name: str = Field(title='Имя')
    last_name: str = Field(title='Фамилия')
