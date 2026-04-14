from pydantic import AliasChoices, BaseModel, Field, ConfigDict


class OvercomplexifyInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )
    task: str = Field(
        ...,
        description="The simple task to over-engineer. E.g. 'make tea', 'send a text', 'buy milk'",
        min_length=2,
        max_length=300
    )
    complexity_tier: int = Field(
        default=3,
        description="How over-engineered should this be? 1=mildly cursed, 5=completely unhinged",
        ge=1,
        le=5
    )
    include_diagram: bool = Field(
        default=True,
        description="Whether to include an ASCII architecture diagram"
    )


class ExplainServiceInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )
    service_name: str = Field(
        ...,
        description="Name of the made-up microservice to explain, e.g. 'TaskIngestionOrchestrator'",
        min_length=2,
        max_length=100
    )
    

class BuzzwordifyInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
        populate_by_name=True,
    )
    text: str = Field(
        ...,
        description="The text to buzzwordify",
        validation_alias=AliasChoices("text", "simple_description"),
    )
