from flask import Flask

app = Flask(__name__)

# members api route
@app.route('/members')
def members():
    return {'members': ['John', 'Mary', 'Bob']}

if __name__ == '__main__':
    app.run(debug=True)