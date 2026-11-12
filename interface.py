from tkinter import *
from aircraft import *
from flight import *
from airline import *
from tkinter import messagebox
from tkinter import filedialog

aircrafts = []
flights = []
airports = []

# ---------- AIRCRAFTS ----------
def ShowAircrafts():
    text = ""
    i = 0
    while i < len(aircrafts):
        text = text + aircrafts[i].callsign + " " + aircrafts[i].type + " " + str(aircrafts[i].capacity) + "\n"
        i = i + 1
    aircraftsLabel.config(text=text)


def LoadAClick():
    filename = filedialog.askopenfilename(title="Aircrafts file")
    if filename == "":
        return
    loaded = LoadAircrafts(filename)
    if len(loaded) == 0:
        messagebox.showerror("Error", "File not found or without valid lines")
        return
    aircrafts.clear()
    i = 0
    while i < len(loaded):
        AddAircraft(aircrafts, loaded[i])
        i = i + 1
    ShowAircrafts()


def AddAClick():
    parts = aircraftEntry.get().split()
    if len(parts) != 4:
        messagebox.showerror("Error", "Format: callsign type capacity airport")
        return
    try:
        capacity = int(parts[2])
    except:
        messagebox.showerror("Error", "Capacity must be a number")
        return
    AddAircraft(aircrafts, Aircraft(parts[0], parts[1], capacity, parts[3]))
    ShowAircrafts()


def RemoveAClick():
    result = RemoveAircraft(aircrafts, aircraftEntry.get().strip())
    if result == -1:
        messagebox.showerror("Error", "Callsign not found")
    ShowAircrafts()


def SaveAClick():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if filename != "":
        SaveAircrafts(aircrafts, filename)


# ---------- FLIGHTS ----------
def ShowFlights():
    text = ""
    i = 0
    while i < len(flights):
        f = flights[i]
        a = f.assignedA
        b = f.assignedB
        if a == "":
            a = "-"
        if b == "":
            b = "-"
        text = text + f.id + " " + f.DepartureAirport + " " + f.ArrivalAirport + " "
        text = text + f.DepartureTime + " " + f.ArrivalTime + " " + str(f.passengers)
        text = text + "  A:" + a + " B:" + b + "\n"
        i = i + 1
    flightsLabel.config(text=text)


def LoadFClick():
    filename = filedialog.askopenfilename(title="Flights file")
    if filename == "":
        return
    loaded = LoadFlights(filename)
    if len(loaded) == 0:
        messagebox.showerror("Error", "File not found or without valid lines")
        return
    flights.clear()
    i = 0
    while i < len(loaded):
        AddFlight(flights, loaded[i])
        i = i + 1
    ShowFlights()


def AddFClick():
    p = flightEntry.get().split()
    if len(p) != 6:
        messagebox.showerror("Error", "Format: id depTime arrTime depAirport arrAirport passengers")
        return
    try:
        passengers = int(p[5])
        TimeToMinutes(p[1])
        TimeToMinutes(p[2])
    except:
        messagebox.showerror("Error", "Passengers must be a number and times HH:MM")
        return
    AddFlight(flights, Flight(p[0], p[3], p[4], p[1], p[2], passengers))
    ShowFlights()


def RemoveFClick():
    result = RemoveFlight(flights, flightEntry.get().strip())
    if result == -1:
        messagebox.showerror("Error", "Flight ID not found")
    ShowFlights()


def SaveFClick():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if filename != "":
        SaveFlights(flights, filename)


def ShowAirports():
    text = ""
    i = 0
    while i < len(airports):
        a = airports[i]
        text = text + a.icao + " " + str(a.latitude) + " " + str(a.longitude) + "\n"
        i = i + 1
    airportsLabel.config(text=text)


def LoadPClick():
    filename = filedialog.askopenfilename(title="Airports file")
    if filename == "":
        return
    loaded = LoadAirports(filename)
    if len(loaded) == 0:
        messagebox.showerror("Error", "File not found or without valid lines")
        return
    airports.clear()
    i = 0
    while i < len(loaded):
        AddAirport(airports, loaded[i])
        i = i + 1
    ShowAirports()


def AddPClick():
    parts = airportEntry.get().split()
    if len(parts) != 3:
        messagebox.showerror("Error", "Format: ICAO latitude longitude")
        return
    try:
        latitude = float(parts[1])
        longitude = float(parts[2])
    except:
        messagebox.showerror("Error", "Latitude and longitude must be numbers")
        return
    AddAirport(airports, Airport(parts[0], latitude, longitude))
    ShowAirports()


def RemovePClick():
    result = RemoveAirport(airports, airportEntry.get().strip())
    if result == -1:
        messagebox.showerror("Error", "ICAO code not found")
    ShowAirports()


def SavePClick():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if filename != "":
        SaveAirports(airports, filename)

def AssignClick(algorithm):
    if len(aircrafts) == 0 or len(flights) == 0:
        messagebox.showerror("Error", "Load the aircrafts and the flights first")
        return
    airline = Airline("Vueling", aircrafts, flights)
    if algorithm == "A":
        AssignA(airline)
    else:
        AssignB(airline)
    ShowFlights()
    assigned = len(AssignedFlights(flights, algorithm))
    unassigned = len(UnassignedFlights(flights, algorithm))
    messagebox.showinfo("Algorithm " + algorithm, "Assigned: " + str(assigned) + "\nNot assigned: " + str(unassigned))


def ShowResultClick(algorithm):
    assigned = AssignedFlights(flights, algorithm)
    unassigned = UnassignedFlights(flights, algorithm)

    text1 = "ASSIGNED FLIGHTS (" + str(len(assigned)) + ")\n"
    i = 0
    while i < len(assigned):
        f = assigned[i]
        text1 = text1 + f.id + " " + f.DepartureAirport + "->" + f.ArrivalAirport + " " + f.DepartureTime + "  " + GetAssigned(f, algorithm) + "\n"
        i = i + 1

    text2 = "NOT ASSIGNED FLIGHTS (" + str(len(unassigned)) + ")\n"
    i = 0
    while i < len(unassigned):
        f = unassigned[i]
        text2 = text2 + f.id + " " + f.DepartureAirport + "->" + f.ArrivalAirport + " " + f.DepartureTime + " pass:" + str(f.passengers) + "\n"
        i = i + 1

    resultWindow = Toplevel(window)
    resultWindow.title("Result of algorithm " + algorithm)
    Label(resultWindow, text=text1, justify=LEFT, anchor="nw", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=N + S + E + W)
    Label(resultWindow, text=text2, justify=LEFT, anchor="nw", bg="white").grid(row=0, column=1, padx=5, pady=5, sticky=N + S + E + W)


def EndOfDayClick(algorithm):
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "Load the aircrafts first")
        return
    filename = filedialog.asksaveasfilename(defaultextension=".txt", title="New aircraft file (end of day)")
    if filename != "":
        airline = Airline("Vueling", aircrafts, flights)
        SaveAircrafts(EndOfDayAircrafts(airline, algorithm), filename)
        messagebox.showinfo("Saved", "File for the next day saved")

def PlotClick():
    if len(flights) == 0:
        messagebox.showerror("Error", "Load the flights first")
        return
    airline = Airline("Vueling", aircrafts, flights)
    PlotFlights(airline)

def RoutesClick(algorithm):
    callsign = aircraftEntry.get().strip()
    if callsign == "":
        messagebox.showerror("Error", "Write the callsign in the aircrafts box")
        return
    airline = Airline("Vueling", aircrafts, flights)
    routes = PlotRoutes(airline, airports, callsign, algorithm)
    if routes == 0:
        messagebox.showerror("Error", "No routes: check the callsign, that the algorithm was run and that the airports are loaded")


# ---------- WINDOW ----------
window = Tk()
window.title("Airline")
window.geometry("900x800")
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=6)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)
window.rowconfigure(5, weight=1)
window.rowconfigure(6, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)

titleLabel = Label(window, text="Airline", font=("Courier", 20, "italic"))
titleLabel.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky=N + S + E + W)

# aircrafts part (left)
aircraftsTitle = Label(window, text="AIRCRAFTS")
aircraftsTitle.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

aircraftsLabel = Label(window, text="", bg="white", justify=LEFT)
aircraftsLabel.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

aircraftEntry = Entry(window)
aircraftEntry.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

LoadAButton = Button(window, text="Load", bg='green', fg="white", command=LoadAClick)
LoadAButton.grid(row=4, column=0, padx=5, pady=5, sticky=N + S + E + W)
AddAButton = Button(window, text="Add", bg='green', fg="white", command=AddAClick)
AddAButton.grid(row=4, column=1, padx=5, pady=5, sticky=N + S + E + W)
RemoveAButton = Button(window, text="Remove", bg='green', fg="white", command=RemoveAClick)
RemoveAButton.grid(row=5, column=0, padx=5, pady=5, sticky=N + S + E + W)
SaveAButton = Button(window, text="Save", bg='green', fg="white", command=SaveAClick)
SaveAButton.grid(row=5, column=1, padx=5, pady=5, sticky=N + S + E + W)


flightsTitle = Label(window, text="FLIGHTS")
flightsTitle.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

flightsLabel = Label(window, text="", bg="white", justify=LEFT)
flightsLabel.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

flightEntry = Entry(window)
flightEntry.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

LoadFButton = Button(window, text="Load", bg='green', fg="white", command=LoadFClick)
LoadFButton.grid(row=4, column=2, padx=5, pady=5, sticky=N + S + E + W)
AddFButton = Button(window, text="Add", bg='green', fg="white", command=AddFClick)
AddFButton.grid(row=4, column=3, padx=5, pady=5, sticky=N + S + E + W)
RemoveFButton = Button(window, text="Remove", bg='green', fg="white", command=RemoveFClick)
RemoveFButton.grid(row=5, column=2, padx=5, pady=5, sticky=N + S + E + W)
SaveFButton = Button(window, text="Save", bg='green', fg="white", command=SaveFClick)
SaveFButton.grid(row=5, column=3, padx=5, pady=5, sticky=N + S + E + W)

Label(window, text="AIRPORTS (ICAO latitude longitude)").grid(row=1, column=4, columnspan=2, sticky=N + S + E + W)
airportsLabel = Label(window, text="", bg="white", justify=LEFT, anchor="nw")
airportsLabel.grid(row=2, column=4, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
airportEntry = Entry(window)
airportEntry.grid(row=3, column=4, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
Button(window, text="Load", bg='orange', fg="black", command=LoadPClick).grid(row=4, column=4, padx=5, pady=5, sticky=N + S + E + W)
Button(window, text="Add", bg='orange', fg="black", command=AddPClick).grid(row=4, column=5, padx=5, pady=5, sticky=N + S + E + W)
Button(window, text="Remove", bg='orange', fg="black", command=RemovePClick).grid(row=5, column=4, padx=5, pady=5, sticky=N + S + E + W)
Button(window, text="Save", bg='orange', fg="black", command=SavePClick).grid(row=5, column=5, padx=5, pady=5, sticky=N + S + E + W)

PlotButton = Button(window, text="Plot flights per hour", bg='grey', fg="black", command=PlotClick)
PlotButton.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky=N + S + E + W)

window.mainloop()