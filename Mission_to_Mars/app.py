from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os

# Create an instance of Flask app
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 
    # Find data
    mars_info = mongo.db.collection.find_one()
    # print("This is the start of mars_info!!!")
    # print(mars_info)

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger scrape function
@app.route("/scrape")

# def scrape():

#     #run the scrape function
#     # mars_data = scrape_mars.scrape_info()
#     mars_data = scrape_mars.scrape_mars_news()
#     console.log(mars_data)

#     #update the Mongo database using update and upsert=True
#     mongo.db.collection.update({}, mars_data, upsert=True)

#     #redirect back to home page
#     return redirect("/")

def scrape(): 

    # Scraped functions
    mars_db = mongo.db.mars_info
    scrape_mars.scrape_mars_news()
    scrape_mars.scrape_mars_image()
    scrape_mars.scrape_mars_weather()
    scrape_mars.scrape_mars_facts()
    scrape_mars.scrape_mars_hemispheres()
    # mars_info={'key1':'test'}
    mars_db.update({}, mars_info, upsert=True)
    mongo.db.collection.update({}, mars_data, upsert=True)

#     return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)