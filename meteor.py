import json
import os

from flask import Flask
from settings import configs
from core import get_countries_with_meteorite_landings_in
from core import get_journal_article_indicator_data_for_multiple
from core import questions


app = Flask(__name__)

#-- CONFIG ------------------------->>>
env = os.environ.get('FLASK_APP_ENV', 'default')
app.config.from_object(configs[env])
#----------------------------------->>>

#-- VIEWS -------------------------->>>
@app.route('/', methods=['GET'])
def index():
    return 'Hello, NASA and the World Bank.'

@app.route('/questions', defaults={'num': None}, methods=['GET'])
@app.route('/questions/<int:num>')
def get_question(num):
    return questions[num] if num else json.dumps(questions)

@app.route('/countries-with-meteorite-landings-in/<int:year>')
def meterorite_landings(year):
    return json.dumps(get_countries_with_meteorite_landings_in(year))
#----------------------------------->>>


if __name__ == '__main__':
    app.run()
