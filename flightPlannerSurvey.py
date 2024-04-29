import random

def getValues():
    starting_point = input("Enter launch coordinates separated by a comma: ")
    start_point = starting_point.split(",")
    for point in start_point:
        print(point)
        point = float(point.strip())
    print(start_point)
    print(type(start_point[0]))
    final_destination = ((37, 73))

    coordinates_input = input("Enter xy coordinates in that order and then the height, all separated by a comma. Or type 'random' for a random path: ")
    if coordinates_input == "random":
        random_numbers = [random.randint(0, 100) for _ in range(21)]
        random_numbers_string = ','.join(map(str, random_numbers))
        print(random_numbers_string)
        coordinates_input = random_numbers_string

    coordinates_list = coordinates_input.split(',')
    coordinates = [int(coord) for coord in coordinates_list]
    coords = [(coordinates[i], coordinates[i+1], coordinates[i+2]) for i in range(0, len(coordinates), 3)]
    print("Coordinates Entered:", coords)
    counter = -1

    flight_code = """
    {
        "fileType": "Plan",
        "geoFence": {
            "circles": [
            ],
            "polygons": [
            ],
            "version": 2
        },
        "groundStation": "QGroundControl",
        "mission": {
            "cruiseSpeed": 15,
            "firmwareType": 12,
            "hoverSpeed": 5,
            "items": [
                {
                    "AMSLAltAboveTerrain": null,
                    "Altitude": 50,
                    "AltitudeMode": 0,
                    "autoContinue": true,
                    "command": 22,
                    "doJumpId": 1,
                    "frame": 3,
                    "params": [
                        15,
                        0,
                        0,
                        null,
                        """ + str(float(start_point[0])) + """,
                        """ + str(float(start_point[1])) + """,
                        50
                    ],
                    "type": "SimpleItem"
                    },
                                {
                        "AMSLAltAboveTerrain": null,
                        "Altitude": 50,
                        "AltitudeMode": 0,
                        "autoContinue": true,
                        "command": 16,
                        "doJumpId": 2,
                        "frame": 3,
                        "params": [
                            0,
                            0,
                            0,
                            null,
                            """ + str(float(start_point[0])) + """,
                            """ + str(float(start_point[1])) + """,
                            50
                        ],
                        "type": "SimpleItem"
                    },
    """
    for coord in coords:
        counter += 1
        if counter != len(coords) - 1:
            flight_code += (
                """
                    {
                        "AMSLAltAboveTerrain": null,
                        "Altitude": 50,
                        "AltitudeMode": 0,
                        "autoContinue": true,
                        "command": 16,
                        "doJumpId": 2,
                        "frame": 3,
                        "params": [
                            0,
                            0,
                            0,
                            null,
                            """ + str(float(start_point[0]) + (.1/9200 * coord[0])) + """,
                            """ + str(float(start_point[1]) + (.1/9200 * coord[1])) +  """,
                            """ + str(coord[2]) + """
                        ],
                        "type": "SimpleItem"
                    },
                """
            )
        else:
            flight_code += (
                """
                    {
                        "AMSLAltAboveTerrain": null,
                        "Altitude": 50,
                        "AltitudeMode": 0,
                        "autoContinue": true,
                        "command": 16,
                        "doJumpId": 2,
                        "frame": 3,
                        "params": [
                            0,
                            0,
                            0,
                            null,
                            """ + str(float(start_point[0]) + (.1/9200 * coord[0])) + """,
                            """ + str(float(start_point[1]) + (.1/9200 * coord[1])) + """,
                            """ + str(coord[2]) + """
                        ],
                        "type": "SimpleItem"
                    }
                """
            )

    flight_code += ("""
            ],
            "plannedHomePosition": [
                """ + start_point[0] + """,
                """ + start_point[1] + """,
                50
            ],
            "vehicleType": 2,
            "version": 2
        },
        "rallyPoints": {
            "points": [
            ],
            "version": 2
        },
        "version": 1
    }
    """)

    return flight_code

# Burger Bowl Coordinates: 33.7785,-84.402

with open("flight_plan2.plan", "w") as flight_plan:
    flight_plan.write(getValues())
