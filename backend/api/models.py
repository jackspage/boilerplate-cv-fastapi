from pydantic import BaseModel


class NoteSchema(BaseModel):
    title: str
    description: str


class NoteDB(NoteSchema):
    id: int

class InferenceResultsSchema(BaseModel):
    image_uuid: str
    model: str
    path_name: str

class InferenceResultsDB(InferenceResultsSchema):
    id: int

