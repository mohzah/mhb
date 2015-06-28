cd $HOME/UPB
source $HOME/.venv/webapp/bin/activate
python manage.py $1 > logs/$1.out 2> logs/$1.err
