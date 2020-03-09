from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)


@app.route("/")
def home():
    return("test")
    # forecasts = mongo.db.collection.find()

    # return render_template("index.html", forecasts=forecasts)


@app.route("/scrape")
def scrape():
    scarped_data = scrape()
    mongo.db.collection.insert_one(scraped_data)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
