from langchain.pydantic_v1 import BaseModel, Field

class Toxicity(BaseModel):
    answer: int = Field(description="Puntuación de toxicidad del usuario")


class Comprehension(BaseModel):
    answer: int = Field(description="Puntuación de comprension del asistente")


class Resolution(BaseModel):
    answer: int = Field(description="Puntuación de resolucion del asistente")


class Summary(BaseModel):
    answer: str = Field(description="Resumen de la siguiente conversacion")

class RatingMetrics(BaseModel):
    toxicity: int = Field(description="Puntuación de toxicidad del usuario")
    comprehension: int = Field(description="Puntuación de comprension del asistente")
    resolution: int = Field(description="Puntuación de resolucion del asistente")

class Title(BaseModel):
    answer: str = Field(description="Titulo de la conversación")

task_classes = {
    "summarization" : Summary,
    "rating_toxicity" : Toxicity,
    "rating_comprehension": Comprehension,
    "rating_resolution": Resolution,
    "rating_metrics": RatingMetrics
}