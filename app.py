from flask import Flask, render_template, request, redirect
import use_data

app = Flask(__name__)


@app.route('/')
def index():
    data = use_data.read_json()
    comments = use_data.only_need_data(use_data.read_json()[1])
    return render_template('index.html', data=reversed(data[0]), comments=comments)


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
        use_data.post_post(request.form.get('name'),
                           request.form.get('content'),
                           int(uid), len(data[1]))
        return redirect(f'/post.html/{uid}')


@app.route('/search.html', methods=['GET', 'POST'])
def search():
    data = use_data.read_json()
    data_output = []
    if request.method == 'GET':
        return render_template('search.html', data=data_output)
    if request.method == 'POST':
        data_output = use_data.post_sort(data[0], str(request.form.get('search_string')))
        comments = use_data.only_need_data(use_data.read_json()[1])
        return render_template('search.html', data=data_output, len=len(data_output), comments=comments,
                               word=str(request.form.get('search_string')))


@app.route('/user-feed.html/<name_user>/')
def user_feed(name_user):
    data = use_data.read_json()
    comments = use_data.only_need_data(use_data.read_json()[1])
    return render_template('user-feed.html', data=use_data.sort_user(data[0], name_user), comments=comments)


@app.route('/tag.html/<tag>')
def tag_page(tag):
    output_post = use_data.sort_tag(use_data.read_json()[0], tag)
    comments = use_data.only_need_data(use_data.read_json()[1])
    return render_template('tag.html', data=output_post, comments=comments, tag=tag)


@app.route('/bookmarks.html')
def bookmarks():
    return render_template('bookmarks.html')


@app.route('/bookmarks.html/add/<id>')
def add_bookmarks(id):
    return redirect('/', code=302)


@app.route('/bookmarks.html/remove/<id>')
def remove_bookmarks(id):
    return redirect('/', code=302)


if __name__ == '__main__':
    app.run(debug=True)
