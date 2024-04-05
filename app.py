from shiny import reactive, render
from shiny.express import ui
import random
from datetime import datetime
from faicons import icon_svg
from collections import deque
import pandas as pd
import plotly.express as px
from shinywidgets import render_plotly
from scipy import stats



UPDATE_INTERVAL_SECS: int = 4

DEQUE_SIZE: int = 5
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

@reactive.calc()
def reactive_calc_combined():
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    #Data generation logic
    temp = round(random.uniform(40, 65), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"temp":temp, "timestamp":timestamp}
    
    #Get the deque and append the new entry
    reactive_value_wrapper.get().append(new_dictionary_entry)

    #Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()

    #For display Convert deque to dataframe for display
    df = pd.DataFrame(deque_snapshot)

    #For display-get the latest dictionary entry
    latest_dictionary_entry = new_dictionary_entry

    #Return a tuple with everything we need
    return deque_snapshot, df, latest_dictionary_entry
    

ui.page_opts(title="PyShiny Express: Live Data From Missouri", fillable=True, )

with ui.sidebar(open="open"):
    ui.h3("Weather for Columbia, MO", class_="text-center", style="color:navy")
    ui.p(
        "A demonstration of real-time temperature readings in Central Missouri.",
        class_="text-center",
    )
    ui.hr()
    ui.h6("Helpful Links:")
    ui.a(
        "Valerie's GitHub Source",
        href="https://github.com/Valpal84/cintel-05-cintel", 
        target="_blank",
    )
    
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")

ui.h2("Current Temperature", style="color:navy")

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("sun"),
        theme="bg-gradient-blue-teal",
    ):
      
        "Current Temperature"
        
        @render.text
        def display_temp():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            theme="bg-gradient-green-blue",
            return f"{latest_dictionary_entry['temp']} F"


        "Seasonal for this time of year"

    with ui.card(full_screen=True):
        ui.card_header("Current Date and Time", style="color:navy")
        @render.text
        def display_time():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"
            

    ui.tags.style(
        ".card-header { color:navy; background:#8FFADB !important;}"
    )
    with ui.card(full_screen=True):
        ui.card_header("Most Recent Readings")

        @render.data_frame
        def display_df():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            pd.set_option('display.width', None)
            return render.DataGrid(df,width="100%")

    with ui.card():
        ui.card_header("Chart with Current Trend")

        @render_plotly
        def display_plotly():
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()

            if not df.empty:
                df["timestamp"] = pd.to_datetime(df["timestamp"])

                fig = px.scatter(df,
                x="timestamp",
                y="temp",
                title="Temperature Readings with Regression Line",
                labels={"temp": "Temperature (°F)", "timestamp": "Timestamp"},
                color_discrete_sequence=["teal"])

                sequence = range(len(df))
                x_vals = list(sequence)
                y_vals = df["temp"]

                slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
                df['best_fit_line'] = [slope * x + intercept for x in x_vals]
                
                #add regresion line to figure
                fig.add_scatter(x=df["timestamp"], y=df['best_fit_line'], mode='lines', name='Regression Line')

                #update layout as needed to customize further
                fig.update_layout(xaxis_title="Time",yaxis_title="Temperature (°F)")
                return fig
            
            


