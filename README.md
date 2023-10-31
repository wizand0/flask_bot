# TODO App

### This is an Introduction to flask. This repo contains a simple web app (TODO) and log for sensors based on arduino uno using flask to get started in flask.
### and also it is a backend for telegrambot for some functions (under constraction)

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Installation](#installation)
- [Built Using](#built_using)

## 🧐 About <a name = "about"></a>

Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.
In this Repo, we will be creating a simple web app (TODO Master).

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The project requires 

- python 3.6 or higher. You can download python from [here](https://www.python.org/downloads/)
- pip. You can download pip from [here](https://pip.pypa.io/en/stable/installing/)
- virtualenv. You can download virtualenv from [here](https://virtualenv.pypa.io/en/latest/installation.html)


## Installation <a name = "installation"></a>

Installing the project is very simple. Just follow the steps below

1. Clone the repo

```
git clone
```

2. Create a virtual environment

```
virtualenv venv
```

3. Activate the virtual environment

```
source venv/bin/activate
```

4. Install the requirements

```
pip install -r requirements.txt
```

5. Run the app

```
python app.py
```

6. Open the app in your browser

```
http://localhost:5000
```



## ⛏️ Built Using <a name = "built_using"></a>

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web Framework
- [Python](https://www.python.org/) - Programming Language
- SQL-ALchemy
- Telegram api


- C:\Users\xabor\PycharmProjects\flask\TODO-app> docker build --tag python-docker .

- PS C:\Users\xabor\PycharmProjects\flask\TODO-app> docker run -d -p 5000:5000 python-docker
"# sensors_blog_and_todo" 
