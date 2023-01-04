# build_files.sh
echo "Building the project ..."
python -m pip install -r requirements.txt

echo "Make Static ..."
python manage.py collectstatic --noinput –clear



