from pydantic import BaseModel, ConfigDict


class CustomBaseModal(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True, extra="forbid", from_attributes=True
    )
