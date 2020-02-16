from flowers_recogn import app, api
from flowers_recogn.cnn_recogn.resources import recognition
from flowers_recogn.flowers_info.resources import flower_list
from flowers_recogn.models import Flower, populate, depopulate

# Routing the resources
# api.add_resource(test_recognition,'/predict/<string:im>')
api.add_resource(recognition, "/predict")
api.add_resource(flower_list, "/flower_list")


if __name__ == "__main__":
    if len(Flower.query.all()) == 0:
        populate()
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)

# WEBSITE DEMO : http://zeus.robots.ox.ac.uk/flower_demo/
