## Run Flask app with automatically change
flask --app app.py --debug run

## Requirement when add a new library
- After add, run this cmd: _pip freeze > requirements.txt_
- Run this cmd if your project is lack of some libraries(as npm install): _pip install -r requirements.txt_


## Explain Folders
# model
Contain model functions to import
# static
Contain the css, script files
# templates
Contain the html files
# app.py
The main run app
