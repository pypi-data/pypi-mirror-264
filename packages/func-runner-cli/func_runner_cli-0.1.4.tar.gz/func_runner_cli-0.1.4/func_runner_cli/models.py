from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Assistant(BaseModel):
    name: str = ''
    instructions: str = ''
    model: str = 'gpt-4'
    code_interpreter: bool = False
    retrieval: bool = False


class FunctionParameter(BaseModel):
    type: str = 'String'
    name: str
    description: str = ''
    required: bool = True


class FunctionDefinition(BaseModel):
    name: str = ''
    description: str = ''
    parameters: list[FunctionParameter] = []


class Project(BaseModel):
    assistant: Assistant = Assistant()
    functions: list[FunctionDefinition] = []


class ProjectSettings(BaseSettings):
    openai_api_key: str
    session_token: Optional[str]
