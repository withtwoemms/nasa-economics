import json
import os

from flask import Flask
from app.settings import configs
from app.core import get_countries_with_meteorite_landings_in
from app.core import get_journal_article_indicator_data_for_multiple
from app.core import questions


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

@app.route('/answers/<int:year>')
def get_answer(year):
    countries = get_countries_with_meteorite_landings_in(year)
    data = get_journal_article_indicator_data_for_multiple(countries, year)
    return json.dumps(sorted(data, key=lambda x: x['num_articles'], reverse=True)[0:5])

@app.route('/countries-with-meteorite-landings-in/<int:year>')
def meteorite_landings(year):
    return json.dumps(get_countries_with_meteorite_landings_in(year))
#----------------------------------->>>


if __name__ == '__main__':
    app.run()
