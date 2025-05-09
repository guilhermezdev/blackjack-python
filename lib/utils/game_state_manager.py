class GameStateManager:
    def __init__(self, initial_state):
        self.state = initial_state
    
    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state