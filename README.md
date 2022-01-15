```python
yum install -y  git  python3
```

```python
cd /usr/local/src/
git clone https://github.com/helmchars/backend-drf-api.git
cd backend-drf-api/
tar fx web.tar.gz 
bash install_nginx.sh 
```


```python
pip3 install pipenv
pipenv --python 3.6.8
pipenv shell

# 进入虚拟环境后
pipenv install -r requirements.txt 
cd ops/
python manage.py makemigrations
python manage.py makemigrations domain
python manage.py migrate 

python manage.py createsuperuser --username admin --email admin@gmail.com

# python manage.py runserver 127.0.0.1:8080
nohup python manage.py runserver 127.0.0.1:8080 >>/var/log/python.log 2>&1 &
```


```python
nohup python test >/dev/null 2>&1 &
```
