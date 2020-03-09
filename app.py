from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)


@app.route("/")
def home():
    data = mongo.db.mars_data.find_one()
    # news_title = data["news_title"]
    # news_p = data["news_p"]
    # featured_image_url = data["featured_image_url"]
    # mars_weather = data["mars_weather"]
    # mars_facts_table = data["mars_facts_table"]
    # hemisphere_image_urls = data["hemisphere_image_urls"]
    return render_template("index.html", mars=data)


@app.route("/scrape")
def scrape():
    mongo.db.mars_data.drop()
    scraped_data = scrape_mars.scrape()
    mongo.db.mars_data.insert_one(scraped_data)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
