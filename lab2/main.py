class Transport(object):
    def __init__(self, s_station, f_station, c_stops, distance):
        self.s_station = s_station
        self.f_station = f_station
        self.c_stops = c_stops
        self.distance = distance
   
    def __str__(self):
        return f"Start: {self.s_station}, Finish: {self.f_station}, Stops: {self.c_stops}, Distance: {self.distance} km"
        end_i = total_chars
        print("".join(c[i:end_i]))

    def __lt__(self, other):
        return self.distance < other.distance

with open("lab2/t.txt", "r", encoding="utf-8") as file:
    transports = []
    for line in file:
        parts = line.split()
        s_station = parts[0]
        f_station = parts[1]
        c_stops = int(parts[2])
        distance = int(parts[3])
        transport = Transport(s_station, f_station, c_stops, distance)
        transports.append(transport)
    transports.sort()


    print("Sorted transports by distance:")
    for t in transports:
        print(t)
    x = int(input("Enter X to find transports with average distance between stops less than X: "))
    count = 0
    for t in transports:
        if t.distance / t.c_stops < x:
            count += 1
    print(f"Number of transports with average distance between stops less than {x}: {count}")
    x_station = input("Enter station X to find transports starting from X: ")
    starting_transports = [t for t in transports if t.s_station == x_station]
    print(f"Transports starting from {x_station}:")
    for t in starting_transports:
        print(t)
    max_stops = max(t.c_stops for t in transports)
    max_stop_transports = [t for t in transports if t.c_stops == max_stops]
    print(f"Transports with maximum number of stops ({max_stops}):")
    for t in max_stop_transports:
        print(t)
