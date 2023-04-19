class Literal:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

class Action:

    def __init__(self, name, preconditions, effects, mutex=[]):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.mutex = mutex

    def __str__(self):
        return self.name


class GraphPlan:

    def __init__(self, initial_state, goal_state, actions):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.actions = actions
        self.literal_layers = [initial_state]
        self.action_layers = []

    def search(self):
        while True:
            if set(self.goal_state).issubset(set(self.literal_layers[-1])):
                for i in self.literal_layers:
                    for j in i:
                        print(j.name)
                    print("Level")
                print("\n")
                for i in self.action_layers:
                    for j in i:
                        print(j.name)
                    print("Next")
                return True
            if len(self.literal_layers) >=2:
                if set(self.goal_state).issubset(set(self.literal_layers[-2])):
                    return False
            self.expand(len(self.literal_layers) - 1)
            self.propagate()

    def expand(self, level):
        action_state = []
        for action in self.actions:
            if all(precondition in self.literal_layers[level] or self.negate(precondition) in self.literal_layers[level] for precondition in action.preconditions):
                if all(action.name not in self.get_mutex_actions(literal) for literal in action.effects):
                    action_state.append(action)
        self.action_layers.append(action_state)

    def propagate(self):
        new_literal_layer = []
        for action_state in self.action_layers:
            for action in action_state:
                for effect in action.effects:
                    if effect not in new_literal_layer:
                        new_literal_layer.append(effect)
        self.literal_layers.append(new_literal_layer)

    def get_mutex_actions(self, literal):
        mutex_actions = []
        for action in self.actions:
            if literal in action.effects:
                mutex_actions += action.mutex
        return mutex_actions

    @staticmethod
    def negate(literal):
        return Literal("~" + literal.name)


# Example usage

# Define the literals
lit_a = Literal("have_cake")
lit_b = Literal("eaten_cake")
neg_a = Literal("~have_cake")
neg_b = Literal("~eaten_cake")
#lit_c = Literal("C")

# Define the actions
action_1 = Action("eat_cake", [lit_a], [neg_a, lit_b])
action_2 = Action("bake_cake", [neg_a], [lit_a])
#action_3 = Action("Action3", [lit_b], [lit_c])

# Define the initial state and goal state
initial_state = [lit_a]
goal_state = [lit_a, lit_b]

# Add mutex for actions
#action_1.mutex = ["Action2", "Action3"]

# Create GraphPlan instance
planner = GraphPlan(initial_state, goal_state, [action_1, action_2])

# Search for a plan
if planner.search():
    print("Goal state is achievable!")
else:
    print("Goal state is not achievable.")
