# EventSpot

## Share your events.
EventSpot is a website for sharing your events. You can create an event, associate pictures, location, date and write about it ! Finally, you can share your creations with your friends.

### Source code
```
git clone git@github.com:HE-Arc/EventSpot.git
```

## Backend (Django)
### Requirements
- Python
### Setup

Create virtual environment
```
# Windows
python -m venv .venv
# Linux
python3 -m venv .venv
```

Activate virtual
```
# Windows
source .venv/Scripts/activate
# Linux
source .venv/bin/activate
```

Install all Python requirements
```
# Windows
pip install -r requirements.txt
# Linux
pip3 install -r requirements.txt
```

Run migrations
```
# Windows
cd eventspot
python manage.py migrate
# Linux
cd eventspot
python3 manage.py migrate
```

Run server
```
# Windows
cd eventspot
python manage.py runserver
# Linux
cd eventspot
python3 manage.py runserver
```

## Frontend (VueJs)
### Requirements
- NodeJs
### Setup


