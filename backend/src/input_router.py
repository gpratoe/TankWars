class InputRouter:
    def __init__(self):
        self.tanks_mediators = {}

    def register_mediator(self, mediator, tank_id):
        self.tanks_mediators[tank_id] = mediator

    def handle_input(self, input, player_id):
        mediator = self.tanks_mediators[player_id]
        if input["shooting"]:
            mediator.notify("Shooting", target_x=input["mouseX"], target_y=input["mouseY"])
        else:
            mediator.notify("MoveTank", x=input["mouseX"], y=input["mouseY"])


