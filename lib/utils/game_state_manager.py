class GameStateManager:
    def __init__(self, initial_state: str):
        self.state = initial_state
    
    def get_state(self) -> str:
        return self.state

    def set_state(self, new_state: str):
        self.state = new_state