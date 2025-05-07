from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Physics Visualization Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Template Configuration
    TEMPLATES_DIR: str = "templates"
    STATIC_DIR: str = "static"
    
    # Visualization Settings
    SUPPORTED_TOPICS: List[str] = [
        "wave",
        "field",
        "circuit",
        "motion"
    ]
    
    # External API Configuration
    LESSON_CONTENT_API: str = "http://ec2-3-88-184-90.compute-1.amazonaws.com:8000/lesson_content_extractor"
    LESSON_EXTRACTOR_API: str = "http://ec2-3-88-184-90.compute-1.amazonaws.com:8000/lesson_extractor"
    QA_API: str = "http://ec2-3-88-184-90.compute-1.amazonaws.com:8000/qa_api"

    class Config:
        case_sensitive = True

settings = Settings() 