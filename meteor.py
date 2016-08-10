import os

from settings import configs
from flask import Flask


app = Flask(__name__)

#-- CONFIG ------------------------->>>
env = os.environ.get('FLASK_APP_ENV', 'default')
app.config.from_object(configs[env])
#----------------------------------->>>

#-- VIEWS -------------------------->>>
@app.route('/', methods=['GET'])
def index():
    return 'Hello, NASA and the World Bank.'
#----------------------------------->>>


if __name__ == '__main__':
    app.run()
