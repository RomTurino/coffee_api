# change this information if it isn't correct
from db_creation import main
POSTGRESQL_LOGIN = 'postgres'
POSTGRESQL_PASSWORD = '123456'

engine = main(POSTGRESQL_LOGIN, POSTGRESQL_PASSWORD)

