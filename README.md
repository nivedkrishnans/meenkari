# meenkari

##Important:
Please modify the meenkari/secret_settings.py during deployment.

##Packages
These are the packages that were intentionally installed :
pip3 install django channels django-registration psycopg2-binary whitenoise dj-database-url
The requirement.txt contains all other packages that came before or with these.

##Databases
By default, the app uses an sqllite database. If you provide a DATABASE_URL environment variable (like in heroku), dj-database-url package will automatically find it and set up the database (check meenkari/secret_settings.py for the same). The requirements.txt contains psycopg2-binary for setting up PostgreSQL; please make appropriate changes for any other database.


##Redis
By default this app doesn not use redis. If you want to use redis, install channels-redis (pip3 install channels-redis). Then install redis on the device and run redis-server. Make changes to the CHANNEL_LAYERS in settings.


