from flask import Flask

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = 'upload'
# app = Flask(__name__, instance_relative_config=True)
# Load the default configuration
# app.config.from_object('config')

# Load the configuration from the instance folder
# app.config.from_pyfile('config.py')




from myapp import views

