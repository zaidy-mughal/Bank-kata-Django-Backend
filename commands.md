python manage.py spectacular --file schema.yml
python manage.py populate_data
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
pip install drf-spectacular
pip install djangorestframework
pip freeze > requirements.txt
pip install -r requirements.txt
