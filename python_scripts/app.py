import flask
app = flask.Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/bye", methods=["POST"])
def bye():
    name = flask.request.get_json()['name']
    response = {}
    response['message'] = "bye {}!".format(name)
    return flask.jsonify(response)

if __name__ == "__main__":
    app.debug = True  # helps us figure out if something went wrong
    app.run()