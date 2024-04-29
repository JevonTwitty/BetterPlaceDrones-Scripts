def getValues():
    flight_type = input("Please enter flight plan type(Survey, corridor scan, structure scan): ")
    fov = int(input("Enter fov: "))
    if flight_type.lower() == "survey":
        starting_point = input("Enter launch coordinates separated by a comma: ")
        start_point = starting_point.split(",")
        for point in start_point:
            print(point)
            point = float(point.strip())
        print(start_point)
        print(type(start_point[0]))
        length = int(input("Enter longitudal length in meters: "))
        width = int(input("Enter width in meters: ")) 
    elif flight_type.lower() == "corridor scan":
        way_points = int(input("Enter number of waypoints: "))
        way_points_hold = way_points
        path_points = []
        while way_points_hold > 0:
            coords = input("Enter coordinates separated by comma: ")
            sep_coords = coords.split(",")
            for coord in sep_coords:
                coord = coord.strip()
            path_points.append((sep_coords[0], sep_coords[1]))
            way_points_hold -= 1
    elif flight_type.lower() == "structure scan":
        pass

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
                        """ + str((float(start_point[0]) - (.001/92 * (0.5 * length - fov)))) + """,
                        """ + str((float(start_point[1]) - (.001/92 * (0.5 * width - fov)))) + """,
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
                            """ + str((float(start_point[0]) - (.001/92 * (0.5 * length - fov)))) + """,
                            """ + str((float(start_point[1]) + (.001/92 * (0.5 * width - fov)))) + """,
                            50
                        ],
                        "type": "SimpleItem"
                    },
    """
    for i in range(int(((length - fov)/fov))):
        if i < (int(((length - fov)/fov)) - 1):
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
                            """ + str((float(start_point[0]) - (.001/92 * (0.5 * length - (i+1) * fov)))) + """,
                            """ + (str((float(start_point[1]) + (.001/92 * (0.5 * width - fov)))) if i%3 == 0 else str((float(start_point[1]) - (.001/92 * (0.5 * width - fov))))) + """,
                            50
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
                            """ + str((float(start_point[0]) - (.001/92 * (0.5 * length - (i+1) * fov)))) + """,
                            """ + (str((float(start_point[1]) + (.001/92 * (0.5 * width - fov)))) if i%3 == 0 else str((float(start_point[1]) - (.001/92 * (0.5 * width - fov))))) + """,
                            50
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

with open("flight_plan.plan", "w") as flight_plan:
    flight_plan.write(getValues())
