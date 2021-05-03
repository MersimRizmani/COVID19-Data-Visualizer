import threading
import tkinter as tk
from tkinter import ttk, font
import pandas as pd
from PIL import Image, ImageTk
from firebase import firebase
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

####################################################
#                 BUILDING THE GUI                 #
####################################################

##############################
#        MAIN WINDOW         #
##############################

window = tk.Tk()
window.title("COVID-19 Data Visualizer")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

##############################
#      MAIN WINDOW END       #
##############################

##############################
#      DATA VISUALIZER       #
##############################

# the figure that will contain the plot
fig = Figure(figsize=(5, 5), dpi=100)
fig.subplots_adjust(left=0.12, bottom=0.15, right=0.95, top=0.95, wspace=0, hspace=0)

# creating the Tkinter canvas
# containing the Matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=window)

# placing the canvas on the Tkinter window
canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")

##############################
#    DATA VISUALIZER END     #
##############################

##############################
#          BUTTONS           #
##############################

fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)

img = Image.open("covidLogo.png")
img = img.resize((150, 150), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(img)
logoLabel = tk.Label(fr_buttons, image=logo, height=150, width=150)
logoLabel.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

welcomeLabel = tk.Label(fr_buttons, text="Welcome to the COVID-19\nData Visualizer!")
welcomeLabel.grid(row=1, column=0, sticky="ew", padx=5)

descriptionLabel = tk.Label(fr_buttons, text="In this application\nyou can visualize\ntime series plots\non various"
                                             " COVID-19\ndata configurations.")
descriptionLabel.grid(row=2, column=0, sticky="ew", padx=5, pady=10)

stateSelectLabel = tk.Label(fr_buttons, text="First select a state:\n(All States for US)")
stateSelectLabel.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

countySelectLabel = tk.Label(fr_buttons, text="Then select a county:\n(All Counties for\nSelected State)")
countySelectLabel.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

metricSelectLabel = tk.Label(fr_buttons, text="Then select what you\nwant to visualize:")
metricSelectLabel.grid(row=7, column=0, sticky="ew", padx=5, pady=5)

buttonLabel = tk.Label(fr_buttons, text="Press the button\nto visualize the\ntime series data!")
buttonLabel.grid(row=9, column=0, sticky="ew", padx=5, pady=5)

btnFont = font.Font(weight="bold", size=20, family="Consolas")
btn = tk.Button(fr_buttons, text="Visualize It!", state=tk.DISABLED, command=None, height=2, width=12, fg='#A5FF33')
btn['font'] = btnFont
btn.grid(row=10, column=0, sticky="ew", padx=5, pady=10)

fr_buttons.grid(row=0, column=0, sticky="nsew")

##############################
#         BUTTONS END        #
##############################

##############################
#        PROGRESS BAR        #
##############################

popup = tk.Toplevel()
popup.geometry("700x100")
popup.grid_columnconfigure(0, weight=1)
popup.grid_rowconfigure(1, weight=1)
tk.Label(popup, text="Loading Data From Database...").grid(row=0, column=0, sticky="nsew")

progress_bar = ttk.Progressbar(popup, orient='horizontal', mode='determinate')
progress_bar['value'] = 0
progress_bar.grid(row=1, column=0, sticky="nsew")

popup.attributes("-topmost", True)

##############################
#      PROGRESS BAR END      #
##############################

####################################################
#               BUILDING THE GUI END               #
####################################################

####################################################
#       ESTABLISH CONNECTION WITH DATABASE         #
####################################################

# Explicitly use service account credentials by specifying the private key
# file.
# storage_client =

# Make an authenticated API request
# buckets = list(storage_client.list_buckets())
# print(buckets)

# cred =
# firebase_admin.initialize_app(cred)

# config = {
#  "apiKey": "apiKey",
#  "authDomain": "covid19tracker-307822.firebaseapp.com",
#  "databaseURL": 'https://covid19tracker-307822-default-rtdb.firebaseio.com/',
#  "storageBucket":
#  "serviceAccount":
# }

# cred
firebase = firebase.FirebaseApplication("https://covid19tracker-307822-default-rtdb.firebaseio.com/", None)
# default_app = firebase_admin.initialize_app(cred)

# database = firebase.database()

####################################################
#     ESTABLISH CONNECTION WITH DATABASE END       #
####################################################

####################################################
#      HELPFUL GLOBAL LISTS/DICTIONARIES           #
####################################################

us_vaccine_data = pd.DataFrame()
state_vacc_data = pd.DataFrame()
us_covid_data = pd.DataFrame()
state_covid_data = pd.DataFrame()
county_covid_data = pd.DataFrame()
state_to_counties = dict()

state_names = ["All States", "Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado",
               "Connecticut", "DC", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois",
               "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan",
               "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska",
               "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon",
               "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
               "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia",
               "Wyoming"]

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

metric_to_label = {
    'positive_daily': "Daily Positive Cases",
    'deaths_daily': "Daily Deaths",
    'total_tests_daily': "Daily Tests Administered",
    'positive_tests': "Total Cases to Date",
    'deaths': "Total Deaths to Date",
    'total_vaccinations': "Total Vaccinations to Date",
    'cases': "Positive Cases to Date",
    'daily_vaccinations': 'Daily Vaccinations',
    'hospitalized_daily': 'Daily Hospitalized'
}

state_metrics = ["positive_daily", "deaths_daily", "total_tests_daily", "positive_tests", "deaths",
                 'total_vaccinations', 'daily_vaccinations']
usa_metrics = ['positive_daily', 'deaths_daily', 'hospitalized_daily', 'total_tests_daily', 'total_vaccinations']
county_metrics = ['cases', 'deaths']

####################################################
#      HELPFUL GLOBAL LISTS/DICTIONARIES END       #
####################################################

####################################################
#          RETRIEVE DATA FROM DATABASE             #
####################################################


def retrieve_data():
    global us_vaccine_data, state_vacc_data, us_covid_data, state_covid_data, county_covid_data

    # retrieve vaccine data for United States
    getUSVacc = firebase.get('/us_vaccines', None)
    us_vaccine_data = pd.DataFrame.from_records(getUSVacc)
    # us_vaccine_data = pd.read_json('cleaned_json/us_vacc.json')
    us_vaccine_data["date"] = pd.to_datetime(us_vaccine_data["date"], format='%Y-%m-%d')
    us_vaccine_data.sort_values('date')
    print(us_vaccine_data.head())

    # update progress bar
    progress_bar['value'] = 20

    # retrieve vaccine data for individual states
    getStateVacc = firebase.get('/state_vaccines', None)
    state_vacc_data = pd.DataFrame.from_records(getStateVacc)
    # state_vacc_data = pd.read_json('cleaned_json/state_vacc.json')
    state_vacc_data["date"] = pd.to_datetime(state_vacc_data["date"], format='%Y-%m-%d')
    state_vacc_data.sort_values('date')
    print(state_vacc_data.head())

    # update progress bar
    progress_bar['value'] = 40

    # retrieve the covid data for the United States
    getUSCovid = firebase.get('/us_covid', None)
    us_covid_data = pd.DataFrame.from_records(getUSCovid)
    # us_covid_data = pd.read_json('cleaned_json/usa_covid.json')
    us_covid_data["date_reported"] = pd.to_datetime(us_covid_data["date_reported"], format='%Y-%m-%d')
    us_covid_data.sort_values('date_reported')
    print(us_covid_data.head())

    # update progress bar
    progress_bar['value'] = 60

    # retrieve the covid data for each state
    getStateCovid = firebase.get('/state_covid', None)
    state_covid_data = pd.DataFrame.from_records(getStateCovid)
    # state_covid_data = pd.read_json('cleaned_json/state_covid.json')
    state_covid_data["date_reported"] = pd.to_datetime(state_covid_data["date_reported"], format='%Y-%m-%d')
    state_covid_data = state_covid_data.sort_values('date_reported', ascending=True)
    print(state_covid_data.head())

    # update progress bar
    progress_bar['value'] = 80

    # retrieve the covid data for each county
    getCountyCovid = firebase.get('/county_covid', None)
    county_covid_data = pd.DataFrame.from_records(getCountyCovid)
    # county_covid_data = pd.read_json('cleaned_json/county_covid.json')
    county_covid_data["date_reported"] = pd.to_datetime(county_covid_data["date_reported"], format='%Y-%m-%d')
    county_covid_data.sort_values('date_reported')
    print(county_covid_data.head())

    # update progress bar
    progress_bar['value'] = 90

    # build a dictionary of states -> list of counties
    for s in state_names:
        if s != "All States":
            list_of_counties = county_covid_data[county_covid_data['state'] == s]
            list_of_counties = list_of_counties['county'].unique().tolist()
            state_to_counties[s] = list_of_counties
        else:
            state_to_counties[s] = ["None"]

    for key, value in state_to_counties.items():
        state_to_counties.get(key).insert(0, "All Counties")

    # update progress bar
    progress_bar['value'] = 100

    # enable all data exploring widgets
    state_select.configure(state=tk.NORMAL)
    btn.configure(command=lambda: plot_data(selected_state, selected_county, selected_metric))

    # close popup
    popup.destroy()


####################################################
#          RETRIEVE DATA FROM DATABASE END         #
####################################################


####################################################
#               PLOTTING THE DATA                  #
####################################################


def plot_data(_selected_state, _selected_county, _selected_metric):
    # adding the subplot
    fig.clear()
    plot1 = fig.add_subplot(111)

    state = _selected_state.get()
    county = _selected_county.get()
    metric = _selected_metric.get()

    if state != "All States":
        if county != "All Counties":
            plot1.set_title(metric_to_label.get(metric) + " " + county + " County, " + state)
            data_to_plot = county_covid_data[county_covid_data['county'] == county]
            data_to_plot = data_to_plot[['date_reported', metric]]
            ax = data_to_plot.plot(x="date_reported", y=metric, kind='line', legend=True, ax=plot1, color='red',
                                   marker='o', fontsize=10)
        else:
            plot1.set_title(metric_to_label.get(metric) + " " + state)
            if metric == 'total_vaccinations' or metric == 'daily_vaccinations':
                data_to_plot = state_vacc_data[state_vacc_data["location"] == us_state_abbrev.get(state)]
                data_to_plot = data_to_plot[['date', metric]]
                ax = data_to_plot.plot(x="date", y=metric, kind='line', legend=True, ax=plot1, color='blue',
                                       marker='o', fontsize=10)
            else:
                data_to_plot = state_covid_data[state_covid_data["state"] == us_state_abbrev.get(state)]
                data_to_plot = data_to_plot[['date_reported', metric]]
                ax = data_to_plot.plot(x="date_reported", y=metric, kind='line', legend=True, ax=plot1, color='green', marker='o',
                                       fontsize=10)
    else:
        plot1.set_title(metric_to_label.get(metric) + " " + "U.S.A.")
        if metric == 'total_vaccinations':
            data_to_plot = us_vaccine_data[['date', metric]]
            ax = data_to_plot.plot(x="date", y=metric, kind='line', legend=True, ax=plot1, color='orange',
                                   marker='o', fontsize=10)
        else:
            data_to_plot = us_covid_data[['date_reported', metric]]
            ax = data_to_plot.plot(x="date_reported", y=metric, kind='line', legend=True, ax=plot1, color='purple',
                                   marker='o', fontsize=10)

    ax.set(xlabel='Date Reported', ylabel=metric_to_label.get(metric))
    canvas.draw()


####################################################
#             PLOTTING THE DATA END                #
####################################################


####################################################
#               UPDATING GUI MENUS                 #
####################################################


def update_metrics(*args):
    if selected_state.get() == "Select State":
        county_select.configure(state=tk.DISABLED)
        metric_select.configure(state=tk.DISABLED)
        btn.configure(state=tk.DISABLED)
    elif selected_state.get() == "All States":
        btn.configure(state=tk.NORMAL)
        metric_select.configure(state=tk.NORMAL)
        county_select.configure(state=tk.DISABLED)
        menu = metric_select['menu']
        menu.delete(0, 'end')

        for metric in usa_metrics:
            menu.add_command(label=metric, command=lambda met=metric: selected_metric.set(met))

        selected_metric.set("Select Metric")
    else:
        btn.configure(state=tk.NORMAL)
        county_select.configure(state=tk.NORMAL)
        metric_select.configure(state=tk.NORMAL)
        menu = metric_select['menu']
        menu.delete(0, 'end')

        for metric in state_metrics:
            menu.add_command(label=metric, command=lambda met=metric: selected_metric.set(met))

        update_counties()
        selected_metric.set("Select Metric")


def update_counties(*args):
    counties = state_to_counties.get(selected_state.get())

    county_menu = county_select['menu']
    county_menu.delete(0, 'end')

    for county in counties:
        county_menu.add_command(label=county, command=lambda c=county: selected_county.set(c))

    selected_county.set("All Counties")


def update_to_county_metrics(*args):
    if selected_county.get() == "Select County":
        btn.configure(state=tk.DISABLED)
        metric_select.configure(state=tk.DISABLED)
    elif selected_county.get() == "All Counties":
        btn.configure(state=tk.NORMAL)
        metric_select.configure(state=tk.NORMAL)
        met_menu = metric_select['menu']
        met_menu.delete(0, 'end')

        for metric in state_metrics:
            met_menu.add_command(label=metric, command=lambda met=metric: selected_metric.set(met))

        selected_metric.set("Select Metric")
    else:
        btn.configure(state=tk.NORMAL)
        metric_select.configure(state=tk.NORMAL)
        met_menu = metric_select['menu']
        met_menu.delete(0, 'end')

        for metric in county_metrics:
            met_menu.add_command(label=metric, command=lambda met=metric: selected_metric.set(met))

        selected_metric.set("Select Metric")


def update_button(*args):
    if selected_metric.get() == "Select Metric":
        btn.configure(state=tk.DISABLED)
    else:
        btn.configure(state=tk.NORMAL)

####################################################
#            UPDATING GUI MENUS END                #
####################################################


####################################################
#            MAIN METHOD/ENTRY POINT               #
####################################################


if __name__ == "__main__":
    # load data on separate thread
    data_loading_thread = threading.Thread(target=retrieve_data)
    window.after(0, data_loading_thread.start())

    # build state select menu
    selected_state = tk.StringVar(window)
    selected_state.set("Select State")
    selected_state.trace('w', update_metrics)

    state_select = tk.OptionMenu(fr_buttons, selected_state, *state_names)
    state_select.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
    state_select.configure(state=tk.DISABLED)

    # build county select menu
    selected_county = tk.StringVar(window)
    selected_county.set("Select County")
    selected_county.trace('w', update_to_county_metrics)

    county_select = tk.OptionMenu(fr_buttons, selected_county, '')
    county_select.grid(row=6, column=0, sticky="ew", padx=10, pady=10)
    county_select.configure(state=tk.DISABLED)

    # build metric select menu
    selected_metric = tk.StringVar(window)
    selected_metric.set("Select Metric")
    selected_metric.trace('w', update_button)

    metric_select = tk.OptionMenu(fr_buttons, selected_metric, '')
    metric_select.grid(row=8, column=0, sticky="ew", padx=10, pady=10)
    metric_select.configure(state=tk.DISABLED)

    window.mainloop()


####################################################
#          MAIN METHOD/ENTRY POINT END             #
####################################################
