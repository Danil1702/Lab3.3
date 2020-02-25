from flask import Flask, render_template, request
import friends_location_map

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map", methods=['POST', 'GET'])
def map():
    user = ''
    if request.method == "POST":
        user = request.form['user']
        friends = friends_location_map.find_friends_location(user)
        return friends_location_map.map_bulding(friends)

if __name__ == "__main__":
    app.run(debug=True)    