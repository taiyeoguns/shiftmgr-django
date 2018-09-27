# ShiftManager

Web application to manage shifts and tasks.

Built with Python and Django.

## Requirements

- Python 3
- [Django](https://www.djangoproject.com/) 2.x
- [Yarn](https://yarnpkg.com/lang/en/)
- [Gulp](https://gulpjs.com/)

## Installation

### Clone Project

```sh
git clone https://github.com/taiyeoguns/shiftmgr-django.git shiftmgr-django
```

### Install Requirements

With a [virtualenv](https://virtualenv.pypa.io/) already set-up, install the requirements with pip:

```sh
pip install -r requirements.txt
```

### Add details in `.env` file

Create `.env` file from example file and maintain necessary details in it e.g. database details etc

```sh
cp .env.example .env
```

### Generate secret key

Generate a secret key to be used by the Django application using the command below:

```sh
python -c "import string,random; uni=string.ascii_letters+string.digits+string.punctuation; print(repr(''.join([random.SystemRandom().choice(uni) for i in range(random.randint(45,50))])))"
```

Copy the generated string and add to the `.env` file created in previous step.


### Run migrations

Create tables in the database:

```sh
python manage.py migrate
```

### Install frontend dependencies

Install `npm` dependencies with Yarn:

```sh
yarn
```

### Generate frontent assets

Run tasks to generate assets:

```sh
gulp
```


### Start the server

Start the Django web server by running:

```sh
python manage.py runserver
```