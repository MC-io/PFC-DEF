class Route:
    def __init__(self):
        self.nodes = []
        self.rank = None
        self.crowding_distance = None
        self.domination_count = None
        self.dominated_solutions = None
        self.features = None
        self.objectives = None

class RouteSet:
    def __init__(self):
        self.routes = []