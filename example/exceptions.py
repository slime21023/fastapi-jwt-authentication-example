from fastapi import HTTPException

class NotImplementedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Not implemented")