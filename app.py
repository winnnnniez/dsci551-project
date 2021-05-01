import json
import re
import yelp_data_processing as res
import instagram_data_processing as insta
from flask import Flask, render_template, request, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "dsci551"


# ============= arguments ===================================================================

# google map embed api key
key='AIzaSyAx0klBrweoSLp6eSUu1K2hWMtlLkiLTHw'

# for restaurants:
la_res = res.get_collection()

# for posts:
la_post = insta.get_collection()
c = la_post.count()
# ===========================================================================================

@app.route('/test')
def index():
    return render_template("index.html", list=l1)

@app.route('/results', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        location = request.form['location']
        session["location"] = location
        if request.form["Submit"] == "Restaurants":
            res_info = res.get_res_info(location, la_res)
            if res_info != []:
                prices, ratings, categories = res.groupByPriceRatingCategory(location, la_res)
                session["prices"] = prices
                session["ratings"] = ratings
                session["categories"] = categories
                message = f"Showing {len(res_info)} results for {location}: "
                return render_template("restaurants.html", loc=location, res_list=res_info, prices=prices, ratings=ratings, categories=categories, msg=message)
            else:
                prices, ratings, categories = [], [], []
                message = f"No results match for {location}."
                return render_template("restaurants.html", loc=location, res_list=res_info, prices=prices, ratings=ratings, categories=categories, msg=message)

        elif request.form["Submit"] == "Instagram Posts":
            post_info = insta.sort_by_likes(location, la_post)
            footer = "Everything is up to date!"
            message = "Results sorted by likes:"
            if insta.get_collection().count() != c:
                footer = "New posts updated!"
            if len(post_info) == 0:
                message = f"No results match for {location}."
            display_list_1 = []
            display_list_2 = []
            display_list_3 = []
            for i in range(0, len(post_info), 3):
                display_list_1.append(post_info[i])
                if i+1 < len(post_info):
                    display_list_2.append(post_info[i+1])
                if i+2 < len(post_info):
                    display_list_3.append(post_info[i+2])
            return render_template("posts.html", loc=location, post_list_1=display_list_1, post_list_2=display_list_2, post_list_3=display_list_3, msg=message, ft=footer)

@app.route('/filtered-restaurants', methods = ['POST', 'GET'])
def filter_res():
    if request.method == 'POST':
        if "location" in session:
            location = session["location"]
            a, b, c = [request.form.getlist('side-checkbox-1'), request.form.getlist('side-checkbox-2'), request.form.getlist('side-checkbox-3')]
            filters = [a, b, c]
            res_info = res.get_filtered_res(location, la_res, filters)
            message = f"Showing {len(res_info)} results for {location}:   -- ratings: {a}, prices: {b}, categories: {c}."
            if res_info == []:
                message = f"No results match for ratings: {a}, prices: {b}, categories: {c}. Try another search to find more restaurants."
            return render_template("restaurants.html", loc=location, res_list=res_info, prices=session["prices"], ratings=session["ratings"], categories=session["categories"], msg=message)

@app.route('/filtered-posts', methods  = ['POST', 'GET'])
def filter_post():
    if request.method == 'POST':
        if "location" in session:
            location = session["location"]
            footer = "Everything is up to date!"
            if request.form['Submit'] == "Most Likes":
                # get info sorted by number of likes
                post_info = insta.sort_by_likes(location, la_post)
                message = "Results sorted by likes:"
            elif request.form['Submit'] == "Most Recent":
                # get info sorted by time
                post_info = insta.sort_by_date(location, la_post)
                message = "Results sorted by time:"
            # message = ""
            if len(post_info) == 0:
                message = f"No results match for {location}."
            display_list_1 = []
            display_list_2 = []
            display_list_3 = []
            for i in range(0, len(post_info), 3):
                display_list_1.append(post_info[i])
                if i+1 < len(post_info):
                    display_list_2.append(post_info[i+1])
                if i+2 < len(post_info):
                    display_list_3.append(post_info[i+2])
        return render_template("posts.html", loc=location, post_list_1=display_list_1, post_list_2=display_list_2, post_list_3=display_list_3, msg=message, ft=footer)

@app.route('/')
def home_page():
    return render_template("search.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
