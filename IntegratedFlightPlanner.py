class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier:
    def __init__(self):
        self.frontier = []
    
    def add(self, newNode):
        self.frontier.append(newNode)

    def remove(self):
        if len(self.frontier) == 0:
            raise Exception("Frontier is empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
    
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
class QueueFrontier(StackFrontier):
    def remove(self):
        if len(self.frontier) == 0:
            raise Exception("Frontier is empty")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
class Obstacles:
    def __init__(self, file_name):
        with open(file_name) as f:
            contents = f.read().splitlines()

        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.layout = []

        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.end = (i, j)
                        row.append(False)
                    elif contents[i][j] == "#":
                        row.append(True)
                    else:
                        row.append(False)
                except IndexError:
                    row.append(False)
            self.layout.append(row)
        
        self.solution = None

    def neighbors(self, state):
        row, col = state

        possible_actions = [
            ("Up", (row - 1, col)),
            ("Down", (row + 1, col)),
            ("Left", (row, col - 1)),
            ("Right", (row, col + 1))
        ]

        actions = []

        for action, (r, c) in possible_actions:
            if 0 <= r < self.height and 0 <= c < self.width and not self.layout[r][c]:
                actions.append((action, (r, c)))
        return actions
    
    def solve(self):
        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None)

        frontier = StackFrontier()
        frontier.add(start)

        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("No Solution")
            
            node = frontier.remove()

            if node.state == self.end:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return self.solution
            
            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
        
class FlightPlanner:
    def __init__(self, file_name, travel_distance):
        obstacles = Obstacles(file_name=file_name)
        solved_obstacles = obstacles.solve()
        self.actions, self.coordinates = solved_obstacles
        self.travel_distance = travel_distance
        print(self.actions)
    
    def create_plan(self, start_point):
        current_positionX, current_positionY = start_point
        self.flight_code = """
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
                                """ + str(float(current_positionX)) + """,
                                """ + str(float(current_positionY)) + """,
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
                                    """ + str(float(current_positionX)) + """,
                                    """ + str(float(current_positionY)) + """,
                                    50
                                ],
                                "type": "SimpleItem"
                            },
        """
        for action in self.actions:
            if action == "Up":
                current_positionY += (self.travel_distance * (.001/92))
            elif action == "Down":
                current_positionY += (self.travel_distance * (.001/92))
            elif action == "Right":
                current_positionX += (self.travel_distance * (.001/92))
            elif action == "Left":
                current_positionX -= (self.travel_distance * (.001/92))
            else:
                raise Exception("Invalid Action")
            
            self.flight_code += (
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
                            """ + str(float(current_positionX)) + """,
                            """ + str(float(current_positionY)) + """,
                            50
                        ],
                        "type": "SimpleItem"
                    },
                """
            )
        # else:
        #     flight_code += (
        #         """
        #             {
        #                 "AMSLAltAboveTerrain": null,
        #                 "Altitude": 50,
        #                 "AltitudeMode": 0,
        #                 "autoContinue": true,
        #                 "command": 16,
        #                 "doJumpId": 2,
        #                 "frame": 3,
        #                 "params": [
        #                     0,
        #                     0,
        #                     0,
        #                     null,
        #                     """ + str((float(start_point[0]) - (.001/92 * (0.5 * length - (i+1) * fov)))) + """,
        #                     """ + (str((float(start_point[1]) + (.001/92 * (0.5 * width - fov)))) if i%3 == 0 else str((float(start_point[1]) - (.001/92 * (0.5 * width - fov))))) + """,
        #                     50
        #                 ],
        #                 "type": "SimpleItem"
        #             }
        #         """
        #     )

        self.flight_code += ("""
                ],
                "plannedHomePosition": [
                    """ + str(float(current_positionX)) + """,
                    """ + str(float(current_positionY)) + """,
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

        with open("integrated_flight_plan.plan", "w") as flight_plan:
            flight_plan.write(self.flight_code)

myPlanner = FlightPlanner("ObstaclesExample.txt", 5)

myPlanner.create_plan((33.7785, -84.402))
