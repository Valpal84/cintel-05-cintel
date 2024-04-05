from shiny import reactive, render
from shiny.express import ui
import random
from datetime import datetime
from faicons import icon_svg

UPDATE_INTERVAL_SECS: int = 1

@reactive.calc()
def reactive_calc_combined():
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
    temp = round(random.uniform(-18, -16), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    latest_dictionary_entry = {"temp": temp, "timestamp": timestamp}
    return latest_dictionary_entry

ui.page_opts(title="PyShiny Express: Live Data (Basics)", fillable=True)

with ui.sidebar(open="open"):
    ui.h2("Antarctic Explorer", class_="text-center")
    ui.p(
        "A demonstration of real-time temperature readings in Antarctica.",
        class_="text-center",
    )

ui.h2("Current Temperature")

@render.text
def display_temp():
    latest_dictionary_entry = reactive_calc_combined()
    return f"{latest_dictionary_entry['temp']} C"

ui.p("look out we hit a hot streak")

icon_svg("snowflake")
icon_svg("snowman")

ui.hr()

ui.h2("Current Date and Time")

@render.text
def display_time():
    latest_dictionary_entry = reactive_calc_combined()
    return f"{latest_dictionary_entry['timestamp']}"
