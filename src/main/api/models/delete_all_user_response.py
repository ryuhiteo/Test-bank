from src.main.api.models.base_model import BaseModel



class DeleteAllUsersResponse(BaseModel):
    message: str
    deleted_count: int