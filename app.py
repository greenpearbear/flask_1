from flask import Flask, render_template
import use_data

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

data = use_data.read_json()
print(data)