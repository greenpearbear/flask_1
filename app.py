from flask import Flask, render_template, request, redirect
import use_data

app = Flask(__name__)


@app.route('/')
def index():
    data = use_data.read_json()
    comments = use_data.only_need_data(use_data.read_json()[1])
    return render_template('index.html', data=data[0], comments=comments)


@app.route('/post.html/<uid>/', methods=['GET', 'POST'])
def post(uid):
    data = use_data.read_json()
    if request.method == 'GET':
        for i in data[0]:
            if i.id == int(uid):
                comments = use_data.comments_sort(int(uid), data[1])
                count_comments = use_data.only_need_data(use_data.read_json()[1])
                if int(uid) in count_comments:
                    return render_template('post.html', data=i, comments=comments,
                                           all_comments=count_comments[int(uid)])
                else:
                    return render_template('post.html', data=i, comments=comments,
                                           all_comments="Нет комментариев")
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_content = request.form.get('content')
        use_data.post_post(new_name, new_content, int(uid), len(data[1]))
        return redirect(f'/post.html/{uid}')


@app.route('/bookmarks.html')
def bookmarks():
    return render_template('bookmarks.html')


@app.route('/user-feed.html')
def user_feed():
    return render_template('user-feed.html')


if __name__ == '__main__':
    app.run(debug=True)
