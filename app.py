from flask import Flask, render_template
import use_data
import logging

app = Flask(__name__)


@app.route('/')
def index():
    data = use_data.read_json()
    return render_template('index.html', data=data[0])


@app.route('/post.html/<uid>/')
def post(uid):
    data = use_data.read_json()
    for i in data[0]:
        if i.id == int(uid):
            return render_template('post.html', data=i)


@app.route('/bookmarks.html')
def bookmarks():
    return render_template('bookmarks.html')


@app.route('/user-feed.html')
def user_feed():
    return render_template('user-feed.html')


if __name__ == '__main__':
    app.run(debug=True)
