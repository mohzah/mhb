source django-venv/bin/activate
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
chown :www-data db.sqlite3 
chmod 664 db.sqlite3
