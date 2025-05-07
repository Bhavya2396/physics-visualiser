from typing import Dict, List
import os
from jinja2 import Environment, FileSystemLoader
from app.core.ai_engine import AIVisualizationEngine, PhysicsConcept, VisualizationParameters

class VisualizationGenerator:
    def __init__(self):
        self.ai_engine = AIVisualizationEngine()
        self.template_env = Environment(
            loader=FileSystemLoader('templates')
        )

    def generate_visualization(self, content: Dict) -> Dict:
        """Generate visualization from course content"""
        # Analyze content using AI engine
        concepts = self.ai_engine.analyze_content(content)
        
        # Generate visualizations for each concept
        visualizations = []
        for concept in concepts:
            visualization = self._create_visualization(concept)
            visualizations.append(visualization)
        
        return {
            "status": "success",
            "data": {
                "visualizations": visualizations,
                "metadata": {
                    "totalConcepts": len(concepts),
                    "conceptTypes": list(set(c.type for c in concepts))
                }
            }
        }

    def _create_visualization(self, concept: PhysicsConcept) -> Dict:
        """Create visualization for a concept"""
        try:
            # Get template files
            template_name = f"{concept.type}/wave_template.html"
            js_template_name = f"{concept.type}/wave_template.js"

            # Generate HTML content
            html_template = self.template_env.get_template(template_name)
            html_content = html_template.render(
                concept=concept,
                params={"javascript": self._get_js_content(concept, js_template_name)}
            )

            return {
                "type": concept.type,
                "html": html_content,
                "concept": concept.dict()
            }

        except Exception as e:
            print(f"Error creating visualization: {str(e)}")
            return self._create_fallback_visualization(concept)

    def _get_js_content(self, concept: PhysicsConcept, template_name: str) -> str:
        """Get JavaScript content from template"""
        try:
            js_template = self.template_env.get_template(template_name)
            return js_template.render(concept=concept)
        except Exception as e:
            print(f"Error loading JavaScript template: {str(e)}")
            return """
                class BasicVisualization {
                    constructor(containerId) {
                        this.container = document.getElementById(containerId);
                    }
                    init() {
                        this.container.innerHTML = 'Basic visualization';
                    }
                }
                const viz = new BasicVisualization('wave-canvas');
                viz.init();
            """

    def _create_fallback_visualization(self, concept: PhysicsConcept) -> Dict:
        """Create a fallback visualization when primary generation fails"""
        return {
            "type": "basic",
            "html": f"""
                <div class="visualization-container">
                    <h2>{concept.name}</h2>
                    <div class="equations">
                        {'<br>'.join(concept.equations)}
                    </div>
                    <div class="variables">
                        {'<br>'.join(f'{var}: {unit}' for var, unit in concept.variables.items())}
                    </div>
                </div>
            """,
            "concept": concept.dict()
        } 