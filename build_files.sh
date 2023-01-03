# build_files.sh
echo "Building the project ..."
python -m pip install -r requirements.txt
echo "Make Migrations ..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo "Make Static ..."
python manage.py collectstatic --noinput --clear




