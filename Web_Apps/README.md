

# DataBase Migration using FLASK-Migrate
1- Set Env Variable
*within the app.py directory*
+ MacOS/Linux  
| export FLASK_APP=app.py
+ Windows  
| set FLASK_APP=app.py
2- Set migration directory
| flask db init 
3- Set migration file
| flask db migrate -m "migration done"
4- Upgrade the migration
| flask db upgrade 