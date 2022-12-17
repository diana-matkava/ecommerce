#### E-commerce project on Flask

## Create and activate virtual environment:
```bash
python3 -m venv venv
venv\Scripts\activate (Windows)
source venv/bin/activate (Linux)
```


## Install dependensies for backend:
```bash
pip install -r requirements.txt
```

## Init DB:
```bash
flask db init
flask db migrate
flask db upgrade
```

## Run a development server:
```bash
flask --debug run
```


## Run a shell in the app context:
```bash
flask shell
```


## Show the routes for the app:
```bash
flask routes
```


