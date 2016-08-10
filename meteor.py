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

@app.route('/questions/<int:num>')
def question(num):
    questions = {
        1: 'Q: In 2008, what are the top 5 countries with documented meteor strikes and published scientific technical journals?',
        2: 'Q: In 2010, what are the top 5 countries with documented meteor strikes and published scientific technical journals?',
        3: 'Q: What countries are unique to both years?',
        4: 'Q: What countries are the same from both years?',
        5: 'Q: Can you infer anything from this data? Why or why not?',
    }
    return questions[num]
#----------------------------------->>>


if __name__ == '__main__':
    app.run()
