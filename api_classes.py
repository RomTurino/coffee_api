from pydantic import BaseModel, Field


class CoffeeAPI(BaseModel):
    #id: int = Field(title='Идентификатор кофе', gt=0)
    coffee_name: str = Field(title='Название кофе')


class PeopleAPI(BaseModel):
    #id: int = Field(title='Идентификатор человека', gt=0)
    first_name:str = Field(title='Имя')
    last_name:str = Field(title='Фамилия')



