# anotherFitnessApp
##to install
run docker-compose up in docker folder
Then docker exec -i -t another-fitness bash
cd /code
python3 manage.py collectstatic
python3 manage.py createsuperuser
