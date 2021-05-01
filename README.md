# Yelp & Instagram Project UI

Search restaurants / instagram posts based on locations

## Notes
All API keys in the uploaded scripts are not usable. If you need to run the scripts, please ask us through our emails. Thanks :) 

## Steps
Install packages in requirements.txt
```bash
pip(3) install -r requirements.txt
```

Run the script
```bash
python(3) app.py
```
After run app.py, enter the web application through http://0.0.0.0:5000/ in your browser.

For streaming data
```bash
python(3) update_instagram_database.py
```


### Description of the functionality:

The users are expected to enter a location in LA and choose to search for either nearby restaurants or instagram posts. The input can be a general location, a zip code, an address, etc. If the users’ input is within the area covered by our database, our website will return a list of results. If the input does not match any result, our UI will display a message on the result page. On the restaurant page, the restaurants are sorted by distance. There is a filter sidebar that users can use to filter the results. On the Instagram page, the posts are sorted by the combination of number of likes and distance by default. The users can choose the posts to be sorted by either most likes or most recent posts.
