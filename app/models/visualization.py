from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class CourseContent(BaseModel):
    topic: str
    subtopics: List[str]
    concepts: List[str]
    key_points: List[str]
    examples: List[Dict[str, str]]

class VisualizationRequest(BaseModel):
    title: str
    concepts: List[Dict[str, str]]
    relationships: Optional[List[Dict[str, str]]] = None

class VisualizationResponse(BaseModel):
    status: str
    data: Dict

class VisualizationTemplate(BaseModel):
    name: str
    description: str
    html_template: str
    js_template: str
    css_template: str
    required_params: List[str]
    optional_params: List[str]

class VisualizationError(BaseModel):
    detail: str 