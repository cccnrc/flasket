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
3. setup [Flasket](https://github.com/cccnrc/flasket) imports in your main application
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

**2.1.** you can now put `ticket` templates inside your `app/templates` folder.
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
