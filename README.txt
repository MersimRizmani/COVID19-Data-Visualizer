Welcome to the COVID-19 Data Visualizer!

This is a simple program that allows you to visualize time series plots on various COVID-19 data configurations. This Python application is integrated with a Realtime Database hosted through Google Firebase, which includes a variety of COVID-19 data. 

The data includes United States COVID data, state-by-state COVID data, as well as county-by-county COVID data. In addition to COVID data, there's also some datasets included that contain vaccine information. COVID-19 data in the database is updated as of 12/06/2020, and vaccine data is updated as of 4/12/2021. 

A folder called 'runnable' was created to make the process of running this application a little simpler for other users. /runnable just contains the main Python script, a text file with the required packages, and an image file referred to in the script. 

To get started with this application and run it, follow the instructions listed in 'application_instructions.txt' in the root directory of this project. 

To view the database (permission needed), follow the instructions listed in 'database_instructions.txt' in the root directory of this project. 

How to use the application:

Once the steps from 'application_instructions.txt' are complete, you are now ready to start visualizing data! Luckily, the features provided by this app are fairly simple:

On the left hand side you'll see 3 options menus, which you will use to configure the data you want to visualize. At the bottom of the left hand side you will see a button labeled "Visualize It!" Some notes on these widgets:

The county selection options menu will remain disabled until a specific state is selected from the state selection options menu. The metric selection will remain disabled until there is a selection in both the county and state selections. The 'Visualize It!' button will remain disabled until there is a selection in all the options menus, or just the state and metric option menus if "All States" is selected. Selecting a state will update the county menu with the corresponding counties for that state. "All Counties" will be selected by default to include data for the whole state. 

To plot the time series data, simple press 'Visualize It!' and a plot will be produced in the canvas on the right side. 

And that's all there is to it! 