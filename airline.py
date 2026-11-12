import matplotlib.pyplot as plt
from aircraft import *
from flight import *
from airport import *


class Airline:
    def __init__(self, name, fleet, operations):
        self.name = name
        self.fleet = fleet
        self.operations = operations


def PrintAirline(airline):
    print("Airline:", airline.name)
    print("Fleet:")
    PrintAircrafts(airline.fleet)
    print("Operations:")
    PrintFlights(airline.operations)


def IsInList(texts, text):
    i = 0
    while i < len(texts):
        if texts[i] == text:
            return True
        i = i + 1
    return False



def AssignA(airline):
    ResetAssignments(airline.operations, "A")
    used = []

    i = 0
    while i < len(airline.operations):
        flight = airline.operations[i]
        found = False
        j = 0
        while j < len(airline.fleet) and found == False:
            aircraft = airline.fleet[j]
            if aircraft.capacity >= flight.passengers and aircraft.location == flight.DepartureAirport and IsInList(used, aircraft.callsign) == False:
                flight.assignedA = aircraft.callsign
                used.append(aircraft.callsign)
                found = True
            j = j + 1
        i = i + 1



def CanChain(first, second):
    arrivalFirst = TimeToMinutes(first.DepartureTime) + FlightDuration(first)
    departureSecond = TimeToMinutes(second.DepartureTime)
    if first.ArrivalAirport == second.DepartureAirport and departureSecond - arrivalFirst >= 120:
        return True
    return False


def AssignB(airline):
    ResetAssignments(airline.operations, "B")
    fleet = airline.fleet

    count = []
    last = []
    i = 0
    while i < len(fleet):
        count.append(0)
        last.append(None)
        i = i + 1

    i = 0
    while i < len(airline.operations):
        flight = airline.operations[i]
        found = False


        j = 0
        while j < len(fleet) and found == False:
            if count[j] == 1 and fleet[j].capacity >= flight.passengers and CanChain(last[j], flight):
                flight.assignedB = fleet[j].callsign
                count[j] = 2
                found = True
            j = j + 1


        j = 0
        while j < len(fleet) and found == False:
            if count[j] == 0 and fleet[j].capacity >= flight.passengers and fleet[j].location == flight.DepartureAirport:
                flight.assignedB = fleet[j].callsign
                count[j] = 1
                last[j] = flight
                found = True
            j = j + 1
        i = i + 1



def EndOfDayAircrafts(airline, algorithm):

    result = []

    i = 0
    while i < len(airline.fleet):
        a = airline.fleet[i]
        location = a.location
        j = 0
        while j < len(airline.operations):
            if GetAssigned(airline.operations[j], algorithm) == a.callsign:
                location = airline.operations[j].ArrivalAirport
            j = j + 1
        result.append(Aircraft(a.callsign, a.type, a.capacity, location))
        i = i + 1
    return result


# ---------- PLOTS ----------
def CountFlightsPerHour(flights):
    counts = []
    h = 0
    while h < 24:
        counts.append(0)
        h = h + 1

    i = 0
    while i < len(flights):
        departure = TimeToMinutes(flights[i].DepartureTime)
        arrival = departure + FlightDuration(flights[i])
        h = 0
        while h < 24:
            if departure < (h + 1) * 60 and arrival > h * 60:
                counts[h] = counts[h] + 1
            if arrival > 1440 and arrival - 1440 > h * 60:
                counts[h] = counts[h] + 1
            h = h + 1
        i = i + 1
    return counts


def PlotFlights(airline):

    scheduled = CountFlightsPerHour(airline.operations)
    countsA = CountFlightsPerHour(AssignedFlights(airline.operations, "A"))
    countsB = CountFlightsPerHour(AssignedFlights(airline.operations, "B"))

    hours = []
    left = []
    right = []
    h = 0
    while h < 24:
        hours.append(h)
        left.append(h - 0.27)
        right.append(h + 0.27)
        h = h + 1

    plt.bar(left, scheduled, width=0.27, label="Scheduled")
    plt.bar(hours, countsA, width=0.27, label="Algorithm A")
    plt.bar(right, countsB, width=0.27, label="Algorithm B")
    plt.xticks(hours)
    plt.xlabel("Hour")
    plt.ylabel("Flights on air")
    plt.title("Flights on air in every hour")
    plt.legend()
    plt.show()


def PlotRoutes(airline, airports, callsign, algorithm):

    routes = 0
    i = 0
    while i < len(airline.operations):
        flight = airline.operations[i]
        if GetAssigned(flight, algorithm) == callsign:
            dep = GetAirport(airports, flight.DepartureAirport)
            arr = GetAirport(airports, flight.ArrivalAirport)
            if dep != None and arr != None:
                plt.plot([dep.longitude, arr.longitude], [dep.latitude, arr.latitude], marker="o")
                plt.text(dep.longitude, dep.latitude, dep.icao)
                plt.text(arr.longitude, arr.latitude, arr.icao)
                routes = routes + 1
            else:
                print("Airport not found for flight", flight.id)
        i = i + 1

    if routes > 0:
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("Routes of " + callsign + " (algorithm " + algorithm + ")")
        plt.grid(True)
        plt.show()
    return routes



if __name__ == "__main__":
    aircrafts = LoadAircrafts("Aircrafts.txt")
    flights = LoadFlights("operations.txt")
    airports = LoadAirports("Airports.txt")
    airline = Airline("Vueling", aircrafts, flights)
    PrintAirline(airline)

    AssignA(airline)
    print("A assigned:", len(AssignedFlights(flights, "A")), "unassigned:", len(UnassignedFlights(flights, "A")))
    AssignB(airline)
    print("B assigned:", len(AssignedFlights(flights, "B")), "unassigned:", len(UnassignedFlights(flights, "B")))

    SaveAircrafts(EndOfDayAircrafts(airline, "A"), "aircrafts_endA.txt")
    SaveAircrafts(EndOfDayAircrafts(airline, "B"), "aircrafts_endB.txt")

    PlotFlights(airline)
    if len(aircrafts) > 0:
        print("Routes drawn:", PlotRoutes(airline, airports, aircrafts[0].callsign, "B"))