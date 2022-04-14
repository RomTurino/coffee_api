#Проект Coffee House

Инструкции по использованию:
1. В директории с проектом выполните команду <code>pip install -r requirements.txt</code>
2. Задайте имя и пароль базы данных в *settings.py*
3. Запустите *main.py* для создания базы данных
4. В файле *db_creation.py* содержится описание таблиц с Column и Sequence сущностями. В функции main создается движок и отправляется запрос на создание таблиц.
5. В файле *api_classes* содержится FastAPI-классы
6. Выполните команду <code> uvicorn main:app --reload</code>