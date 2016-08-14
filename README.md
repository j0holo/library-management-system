# Library managment system

A library managment system written with Flask and Peewee. Currently work in progress. Currently only a couple of administration pages work.

### To-Do

- [x] Laying out all database models
- [ ] Write accompanying methods for models
- [ ] Write the administration pages
- [ ] Change the way database configuration is being configured
        (currently not safe)
- [ ] Program login portal for adminstration pages
- [ ] Write customer pages e.g.:
    -  book page
    -  account information page
    -  review page
    -  home page
- [ ] Connect customer login page so only logged in customer can write reviews
    and  view their own account information
- [ ] Give the site some style with CSS
- [ ] Insert demo data into the database to improve the demo experience

### How to run the demo version

Terminal commands are denoted by:```$```

- clone the repo
- ```$ pip install -r requiremenets.txt```
- ```$ sudo apt install mariadb-server``` or mysql-server
- ```$ export DB_HOST="localhost"``` or you can use another IP address from
    where the database is running from.
- Create two users for the database. The users that are configured for testing
    are *development* and *unittest*. Their passwords are *devpassword* and
    *test_db*.

_*PLEASE ONLY USE THESE SETTINGS FOR LOCAL TESTING! NEVER USE USERNAMES AND PASSWORDS PROVIDED BY A MAINTAINER FOR PRODUCTION USE!*_

- Create two databases with the names *devdatabase* and *test_db* where
*development* has access to *devdatabase* and *unittest* has access to *test_db*.
- Run ```$ python models.py``` to create the tables in the databases
- Run ```$ python unittests.py``` to run the unittests
- Run ```$ python app.py``` to start the server. The website is available on 127.0.0.1:5000.

_*Currently this is not optimal at all, configuring the databases should be way more secure*_

### License

This project is licensed under the MIT license, see LICENSE for more info.
