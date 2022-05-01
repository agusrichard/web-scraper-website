<center><h1>Web Scraper Website</h1></center>

### Table of Contents:
- [Description](#description)
- [GIF of what you'll see on this app](#gif-of-what-youll-see-on-this-app)
- [Installation/Development](#installationdevelopment)

## Description

This application is a simple web application written in Python using Django Web Framework.
It scrapes articles from Medium and show all those articles on this application home page.
There are two ways this application scrapes Medium articles, the first one is using a scheduled task (running every day) and the second one is by running a scraping task manually. This application leverages Selenium to scrape and Celery to run asynchronous background task (could be a scheduled one too).

## GIF of what you'll see on this app
<img src="./contents/app.gif" alt="App GIF" width="700" height="390" />

## Installation/Development
1.  Fork this repository to your local machine.
2.  Create a .env file in the root directory.
3.  Provide environment variables to .env file (below is an example you can use):
    ```text
    SECRET_KEY=SECRET_KEY
    DEBUG=True
    DB_NAME=db
    DB_USER=user
    DB_PASSWORD=password
    DB_HOST=db
    DB_PORT=5432
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    SCRAPE_URL=https://medium.com/search?q=programming
    ```
4.  Run all containers by running:
    ```shell
    docker-compose up
    ```
5.  Django development web server will run on port 8000.
6.  You can interact with the app at this point. Happy using it!