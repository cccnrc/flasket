# Flasket: Flask(tick)et

This is a Ticket service for your [Flask](https://flask.palletsprojects.com/en/2.0.x/) application.


---
## Blueprint

We developed this as a [Blueprint](https://flask.palletsprojects.com/en/2.0.x/blueprints/) branch: you only need to copy our `ticket` folder in you application and setup a couple of `import` and you will have your ticketing system on!

[Blueprint](https://flask.palletsprojects.com/en/2.0.x/blueprints/) is integrated in [Flask](https://flask.palletsprojects.com/en/2.0.x/) and allows you to logically organize your different application services (e.g. tickets, api, etc.) in different folders, making development (and your life) extremely easier! :sunglasses:

It also has the advantage of creating a URL with the service name before any of the service's endpoints! Ex. `localhost/<service>/<endpoint>`

---
## Installation

In order to implement [Flasket](https://github.com/cccnrc/flasket) in your application you need to take 4 simple steps:
1. clone [Flasket](https://github.com/cccnrc/flasket)
2. copy [Flasket](https://github.com/cccnrc/flasket) folders in your Flask application
3. setup [Flasket](https://github.com/cccnrc/flasket) imports in your Flask application
4. edit [Flasket](https://github.com/cccnrc/flasket) `forms.py` to reflect your application
5. update your application database with [Flasket](https://github.com/cccnrc/flasket) tables
6. use [Flasket](https://github.com/cccnrc/flasket) :sunglasses:

<br/>

### 1. clone [Flasket](https://github.com/cccnrc/flasket)
**1.1.** set your application main folder as `APP_DIR` environment variable:
```
APP_DIR=<your-Flask-application-directory>
```
- ***note***: replace `<your-Flask-application-directory>` with the path to your Flask application directory

<br />

**1.2.** clone the [Flasket](https://github.com/cccnrc/flasket) repository (outside your application folder):
```
cd
git clone https://github.com/cccnrc/flasket.git
FLASKET_DIR=$( pwd )/flasket
```
- **Important**: if you use different terminal windows environment variables ***are not inherited***. Thus, you need to ***reset*** them (`APP_DIR`, `FLASKET_DIR`) for any new terminal window you will use.


<br/>
<br/>

### 2. copy [Flasket](https://github.com/cccnrc/flasket) folders in your Flask application
**2.1.** we want to create a `ticket` blueprint branch for our application. We first need to create the folder in your application structure: you can simply copy into `app/` the `ticket` folder of this repository:
```
cp -r $FLASKET_DIR/ticket $APP_DIR/app/
```
Assuming your application main folder is called `app` you should get this structure:
```
$APP_DIR
├── app
│   ├── ticket
│   │   ├── __init__.py
│   │   ├── email.py
│   │   ├── forms.py
│   │   └── routes.py
│   └── ...rest of app files...
```

**2.2.** you can now put `ticket` templates inside your `app/templates` folder.
This way you will have all templates related to this service inside that folder:
```
cp -r $FLASKET_DIR/templates/ticket $APP_DIR/app/templates/
```
Your application should look similar to this now:
```
$APP_DIR
├── app
│   ├── ticket
│   │   ├── __init__.py
│   │   ├── email.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── templates
│   │   ├── ... rest of your templates ...
│   │   └── ticket
│   │       ├── index.html
│   │       ├── all.html
│   │       ├── ticket.html
│   │       ├── ticket_reply.html
│   │       ├── ticket_submit.html
│   │       └── user.html
```

<br/>
<br/>

### 3. setup [Flasket](https://github.com/cccnrc/flasket) imports in your Flask application
**3.1.** if you take a look at `ticket/__init__.py` you see that this file simply defines a ticket `bp` (Blueprint) and imports all endpoints specified in its `routes.py` file:
```
from flask import Blueprint

bp = Blueprint('ticket', __name__)

from app.ticket import routes
```

**3.2.** import `ticket_bp` in your main application `app/__init__.py` file:
```
from app.ticket import bp as ticket_bp
app.register_blueprint( ticket_bp, url_prefix='/ticket' )
```
- **Important**: this step depends on how you are ***starting*** your Flask application. As example, we use a `create_app(config_class=Config)` function specified in `app/__init__.py` that we import into `main.py` and starts it whenever the application is launched:
```
from app import create_app, db

app = create_app()
```
- so we store the `app.ticket import` into that function in `app/__init__.py`:
```
from flask import Flask
from config import Config     ### variables store in app/config.py
# ... rest of imports ... #

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    # ... rest of function code ... #

    from app.ticket import bp as ticket_bp
    app.register_blueprint( ticket_bp, url_prefix='/ticket' )

    # ... rest of function code ... #

```
- this configuration will put into your URL `/ticket` before any of the endpoint inherited from `app/ticket/routes.py` and your website will look much more professional :sunglasses:


<br/>
<br/>

### 4. edit [Flasket](https://github.com/cccnrc/flasket) `forms.py` to reflect your application
[Flasket](https://github.com/cccnrc/flasket) tickets come with several fields that you find in `ticket/forms.py`:
- *urgency*: the level of importance of the ticket (`urgency_choices`)
- *application*: which application the ticket is referring to (`ticket_app`)
- *argument*: which topic the ticket is referring to (`ticket_arg`)

You can edit those as you wish, add/remove categories etc. to reflect your application needs

<br/>
<br/>

### 5. update your application database with [Flasket](https://github.com/cccnrc/flasket) tables
**5.1.** modify your `models.py` accordingly to what is specified in [ticket-models-instructions.txt](https://github.com/cccnrc/flasket/blob/main/ticket-models-instructions.txt): you basically have to create `Ticket`, `TicketReply`, and `user_tickets` Tables, and add `admin`, `tickets`, `ticket_replies`, and `tickets_followed` to your `User` Table
You will find detailed instructions for this in [ticket-models-instructions.txt](https://github.com/cccnrc/flasket/blob/main/ticket-models-instructions.txt)

**5.2.** once `models.py` is updated, you need to apply those changes to your application database. Ex. if using `flask db`:
```
flask db migrate -m "added ticket tables"
flask db upgrade
```
or whatever method you are using for your Falsk application database management

- ***note***: if you add/remove columns etc. in `ticket/forms.py` you have to reflect such changes into `models.py`

<br/>
<br/>

### 6. use [Flasket](https://github.com/cccnrc/flasket) for your tickets! :sunglasses:
If nothing went wrong you should be able to launch your application and use your brand new ticketing system!
