# import dependencies
# The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
# The second line says we'll use PyMongo to interact with our Mongo database.
# The third line says that to use the scraping code, we will convert from Jupyter notebook to Python.
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up Flask app
app = Flask(__name__)

# Tell python how to connect to Mongo using PyMongo
# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)


# Set up app routes

# Define route for HTML page

# @app.route("/"), tells Flask what to display when we're looking at the home page, 
# index.html (index.html is the default HTML file that we'll use to display the content we've scraped).
@app.route("/")
def index():
    # mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database, 
    # which we will create when we convert our Jupyter scraping code to Python Script. We will also assign that path to themars variable for use later
    mars = mongo.db.mars.find_one()
    # return render_template("index.html" tells Flask to return an HTML template using an index.html file. We'll create this file after we build the Flask routes.
    # , mars=mars) tells Python to use the "mars" collection in MongoDB
    return render_template("index.html", mars = mars)

# Set up scraping route
@app.route("/scrape")
# The first line, @app.route(“/scrape”) defines the route that Flask will be using. This route, “/scrape”, will run the function that we create just beneath it.
def scrape():
    # assign a new variable that points to our Mongo database
    mars = mongo.db.mars
    # created a new variable to hold the newly scraped data
    # In this line, we're referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook
    mars_data = scraping.scrape_all()
    # update the database using .update() function with the following syntax: .update(query_parameter, data, options)
    # We're inserting data, so first we'll need to add an empty JSON object with {} in place of the query_parameter. 
    # Next, we'll use the data we have stored in mars_data. 
    # Finally, the option we'll include is upsert=True. This indicates to Mongo to create a new document if one doesn't already exist, 
    # and new data will always be saved (even if we haven't already created a document for it).
    mars.update({}, mars_data, upsert = True)
    # add a redirect after successfully scraping the data that navigates back to homepage with updated content
    return redirect('/', code = 302)

# Run Flask app
if __name__ == "__main__":
   app.run()