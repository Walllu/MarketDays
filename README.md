# MarketDays
MarketDays is a trading application with real rewards.<br/> 
Spring cleaning? Take anything you don't want anymore, and take part in a daily local market trading session! <br/> <br/> 
Find items you want, and propose trades. Swap item cards throughout the day, and use them to find the perfect deal! <br/> <br/> 
Or just kick back, and watch offers come pouring in! At the end of the day, take your spring cleaning to the market location, and exchange your items! <br/> <br/> 
After all, "One man's trash is another man's treasure." <br/> 

## Deploying on your machine
We recommend installing the latest version of Python 3.X, as this project runs on Python3. 
Open your shell and navigate to your directory of choice, and run `git clone https://github.com/Walllu/MarketDays.git` to clone the repository. Optionally, you can make a virtual environment to house the requirements of this project, but it is not required. Within your virtual environment, run `pip install -r requirements.txt` to download the project requirements.
From within the project's main directory, run `python manage.py makemigrations` then `python manage.py migrate` to initialize the database. Then run `python population_script.py` to populate the database.
This process takes less than a minute, and once completed, you can run the project with `python manage.py runserver`.
Congratulations! You have MarketDays up and running on the Django development server, on your own machine!


## Milestones

- [X] Design the models
  - [X] Look at the requirements spec
	- [X] Make an ER diagram --> translate this into Django's ORM
	- [X] Implement models 
    - [X] Test with the admin interface
    - [X] Create a plausible testing scenario (using the user personas and their info)
    - [X] Write tests for this
	

- [X] Design views and the templates (these are interlinked in many ways - open communication on this is necessary)
	- [X] Design a site map --> make URL mapping decisions (including URL "name")
	- [X] Design and draw up wireframes of each page
	- [X] Implement user login and sign up functionality --> 
		Pages built from here onwards, all users need to be authenticated to view
	- [X] Assign each group member a particular set of pages to create
		- Tests (write tests first and continuously!)
		- Template
		- View
		- URL map
	- [X] Merge pages in style (CSS & Javascipt)
	- [X] Polish up user experience
	- [X] Test to make sure the application actually works as intended


