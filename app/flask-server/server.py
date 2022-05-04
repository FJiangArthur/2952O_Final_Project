from flask import Flask

from realsense_camera import *
from mask_rcnn import *

from measure_object_distance import run

app = Flask(__name__)


@app.route('/members')
def members():
    return {'members': ['John', 'Mary', 'Bob']}


@app.route('/realsense', methods=['POST'])
def realsense():
    print("hit realsense member")

    # run measure_object_distance
    yield run()

    # return "completed"


if __name__ == '__main__':
    app.run(debug=True)
