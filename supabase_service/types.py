class GenericResponse:
    def __init__(self, status: int, message: str, data: object = None, count: int = None):
        self.status = status
        self.message = message
        self.data = data
        self.count = count

    def __str__(self):
        return f"{self.status} - {self.message} - {self.data} - {self.count}"
