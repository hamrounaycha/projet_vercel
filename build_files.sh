# build_files.sh
echo "Building the project ..."
pip install -r requirements.txt

echo "Make Static ..."
python manage.py collectstatic

