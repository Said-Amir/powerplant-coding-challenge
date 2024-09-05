# app/errors/error_handler.py
class ValidationError(Exception):
    def __init__(self, message="Invalid data provided"):
        self.message = message
        self.status_code = 400
        super().__init__(self.message)

class InsufficientCapacityError(Exception):
    def __init__(self, message="Insufficient capacity to satisfy the load"):
        self.message = message
        self.status_code = 422
        super().__init__(self.message)
