from enum import Enum
from typing import Literal, Sequence, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated


class ActionType(str, Enum):
    OVERRIDE = "OVERRIDE"
    PASSTHROUGH = "PASSTHROUGH"


class BaseAction(BaseModel):
    type: ActionType = Field(description="Type of action to take.")


class OverrideAction(BaseAction):
    type: Literal[ActionType.OVERRIDE] = ActionType.OVERRIDE
    choices: Sequence[str] = Field(
        description="List of choices to override the response with. If there are multiple choices, one will be chosen at random when applying this action.",
        min_length=1,
    )


class PassthroughAction(BaseAction):
    type: Literal[ActionType.PASSTHROUGH] = ActionType.PASSTHROUGH


Action = Annotated[Union[OverrideAction, PassthroughAction], Field(discriminator="type")]
