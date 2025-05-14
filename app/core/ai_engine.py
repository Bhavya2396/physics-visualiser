from typing import Dict, List, Optional
from pydantic import BaseModel

class PhysicsConcept(BaseModel):
    name: str
    type: str
    description: str
    equations: List[str]
    key_points: List[str]
    variables: Dict[str, str] = {}

class VisualizationParameters(BaseModel):
    type: str
    dimensions: str = "2d"
    components: List[str] = []
    interactive_elements: List[str] = []
    data_mappings: Dict[str, str] = {}
    javascript: str = ""

class AIVisualizationEngine:
    def __init__(self):
        self.concept_templates = {
            "wave": {
                "components": ["oscillator", "wave-front", "particle-motion"],
                "variables": {"frequency": "Hz", "amplitude": "m", "wavelength": "m"},
                "interactions": ["frequency-control", "amplitude-control"]
            },
            "field": {
                "components": ["field-lines", "vectors", "equipotential"],
                "variables": {"strength": "N/C", "distance": "m"},
                "interactions": ["source-control", "field-strength"]
            }
        }

    def analyze_content(self, content: Dict) -> List[PhysicsConcept]:
        concepts = []
        for concept_data in content.get("concepts", []):
            concept_type = self._identify_concept_type(concept_data)
            if concept_type:
                concept = PhysicsConcept(
                    name=concept_data.get("name", ""),
                    type=concept_type,
                    description=concept_data.get("description", ""),
                    equations=concept_data.get("equations", []),
                    key_points=concept_data.get("key_points", []),
                    variables=self._get_concept_variables(concept_type)
                )
                concepts.append(concept)
        return concepts

    def _identify_concept_type(self, concept_data: Dict) -> str:
        name = concept_data.get("name", "").lower()
        if any(word in name for word in ["wave", "oscillation", "frequency"]):
            return "wave"
        elif any(word in name for word in ["field", "force", "potential"]):
            return "field"
        return "wave"  # default to wave for testing

    def _get_concept_variables(self, concept_type: str) -> Dict[str, str]:
        template = self.concept_templates.get(concept_type, {})
        return template.get("variables", {}) 