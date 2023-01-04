# build_files.sh
echo "Building the project ..."
python -m pip install -r requirements.txt

echo "Make Static ..."
python3.8 manage.py collectstatic --noinput –clear



