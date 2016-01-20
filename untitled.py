from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import json, sqlalchemy

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re


re_alpha = re.compile('[^a-zA-Z ]')
stops = set(stopwords.words('english'))

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/')
def hello_world():
    return render_template("next_word.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = request.form
    text = form["text"]

    print text

    text = text.lower()
    text = re_alpha.sub('', text)

    print text

    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    tokens = [token for token in tokens if not token in stops]

    while len(tokens) < 3:
        tokens.insert(0, '')

    # temp = text.split()

    tokens_len = len(tokens)

    l1 = tokens[tokens_len - 3]
    l2 = tokens[tokens_len - 2]
    l3 = tokens[tokens_len - 1]

    f2 = 100
    f3 = 5
    f4 = 2

    rows = ()

    while len(rows) < 5:

        query = "EXEC sp_predict @l1='{l1}', @l2='{l2}', @l3='{l3}', @f2={f2}, @f3={f3}, @f4={f4}".format(
                    l1=l1, l2=l2, l3=l3, f2=f2, f3=f3, f4=f4)
        rows = db.session.execute(query).fetchall()

        if f2 > 1:
            f2 = abs(f2/2)
        else:
            f2 = 1
        if f3 > 1:
            f3 += -2
        else:
            f3 = 1
        f4 = 1

        print query

    return json.dumps([dict(r) for r in rows], default=alchemyencoder)


@app.route('/next_word', methods=['GET', 'POST'])
@crossdomain(origin='*')
def next_word():
    form = request.form
    text = form["text"]

    print text

    text = text.lower()
    text = re_alpha.sub('', text)

    print text

    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    tokens = [token for token in tokens if not token in stops]

    while len(tokens) < 3:
        tokens.insert(0, '')

    # temp = text.split()

    tokens_len = len(tokens)

    l1 = tokens[tokens_len - 3]
    l2 = tokens[tokens_len - 2]
    l3 = tokens[tokens_len - 1]

    f2 = 100
    f3 = 5
    f4 = 2

    rows = ()

    while len(rows) < 5 and f2 > 1:

        query = "EXEC sp_next_word @l1='{l1}', @l2='{l2}', @l3='{l3}', @f2={f2}, @f3={f3}, @f4={f4}".format(
                    l1=l1, l2=l2, l3=l3, f2=f2, f3=f3, f4=f4)

        print query

        rows = db.session.execute(query).fetchall()

        if f2 > 1:
            f2 = abs(f2/2)
        else:
            f2 = 1
        if f3 > 1:
            f3 += -2
        else:
            f3 = 1
        f4 = 1

    words = []
    for r in rows:
        word = str(r.l4)
        words.append(word)

    unique_words = list(set(words))

    print unique_words

    response = json.dumps(unique_words)

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



if __name__ == '__main__':
    app.run()
