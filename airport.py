class Airport:
    def __init__(self, icao, latitude, longitude):
        self.icao = icao
        self.latitude = latitude        # decimal degrees (float)
        self.longitude = longitude      # decimal degrees (float)


def PrintAirport(airport):
    # Prints in console the data of the airport
    print(airport.icao, airport.latitude, airport.longitude)


def LoadAirports(filename):
    # Returns a list of airports read from the file. Empty list if the file does not exist
    airports = []
    try:
        file = open(filename, "r")
    except:
        return airports

    lines = file.readlines()
    file.close()

    i = 0
    while i < len(lines):
        parts = lines[i].split()
        if len(parts) == 3:
            try:
                latitude = float(parts[1])
                longitude = float(parts[2])
                airports.append(Airport(parts[0], latitude, longitude))
            except:
                print("Line ignored:", lines[i])
        i = i + 1
    return airports


def SaveAirports(airports, filename):
    # Saves the airports in the file
    file = open(filename, "w")
    i = 0
    while i < len(airports):
        a = airports[i]
        file.write(a.icao + " " + str(a.latitude) + " " + str(a.longitude) + "\n")
        i = i + 1
    file.close()


def PrintAirports(airports):
    # Prints in console all the airports in the list
    i = 0
    while i < len(airports):
        PrintAirport(airports[i])
        i = i + 1


def AddAirport(airports, airport):
    # Adds the airport to the list
    airports.append(airport)


def RemoveAirport(airports, icao):
    # Removes the airport with that ICAO code. Returns 0 if removed, -1 if not found
    i = 0
    while i < len(airports):
        if airports[i].icao == icao:
            airports.remove(airports[i])
            return 0
        i = i + 1
    return -1


def GetAirport(airports, icao):
    # Returns the airport with that ICAO code, or None if it is not in the list
    i = 0
    while i < len(airports):
        if airports[i].icao == icao:
            return airports[i]
        i = i + 1
    return None


# test section
if __name__ == "__main__":
    airports = LoadAirports("Airports.txt")
    PrintAirports(airports)
    AddAirport(airports, Airport("TEST", 10.5, 20.5))
    print(RemoveAirport(airports, "TEST"))       # 0
    print(RemoveAirport(airports, "ZZZZ"))       # -1
    airport = GetAirport(airports, "LEBL")
    if airport != None:
        PrintAirport(airport)
    SaveAirports(airports, "airports_saved.txt")