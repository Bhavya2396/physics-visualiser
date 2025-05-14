from typing import Dict, Optional
from jinja2 import Environment, FileSystemLoader
from app.core.config import settings
from app.models.visualization import (
    CourseContent,
    VisualizationRequest,
    VisualizationResponse,
    VisualizationTemplate
)

class VisualizationService:
    def __init__(self):
        self.template_env = Environment(
            loader=FileSystemLoader(settings.TEMPLATES_DIR)
        )
        self.visualization_templates = self._load_visualization_templates()

    def _load_visualization_templates(self) -> Dict[str, VisualizationTemplate]:
        """Load all visualization templates from the templates directory"""
        templates = {}
        for topic in settings.SUPPORTED_TOPICS:
            try:
                # Load template configurations
                templates[topic] = VisualizationTemplate(
                    name=topic,
                    description=f"Interactive visualization for {topic.replace('_', ' ')}",
                    html_template=f"{topic}/index.html",
                    js_template=f"{topic}/script.js",
                    css_template=f"{topic}/styles.css",
                    required_params=["course_content"],
                    optional_params=["interactive", "additional_params"]
                )
            except Exception as e:
                print(f"Error loading template for {topic}: {str(e)}")
        return templates

    async def generate_visualization(
        self,
        request: VisualizationRequest
    ) -> VisualizationResponse:
        """Generate visualization based on course content"""
        # Get the appropriate template
        template = self.visualization_templates.get(request.visualization_type)
        if not template:
            raise ValueError(f"Unsupported visualization type: {request.visualization_type}")

        # Process course content
        processed_content = self._process_course_content(request.course_content)

        # Generate visualization components
        html_content = self._generate_html(template, processed_content, request.additional_params)
        js_content = self._generate_js(template, processed_content, request.additional_params)
        css_content = self._generate_css(template, processed_content)

        # Determine dependencies
        dependencies = self._get_dependencies(request.visualization_type)

        return VisualizationResponse(
            html_content=html_content,
            js_content=js_content,
            css_content=css_content,
            dependencies=dependencies,
            instructions="Instructions for embedding the visualization"
        )

    def _process_course_content(self, content: CourseContent) -> Dict:
        """Process and structure course content for visualization"""
        return {
            "topic": content.topic,
            "subtopics": content.subtopics,
            "concepts": content.concepts,
            "key_points": content.key_points,
            "examples": content.examples,
            "structured_data": self._structure_content_for_visualization(content)
        }

    def _structure_content_for_visualization(self, content: CourseContent) -> Dict:
        """Structure content specifically for visualization"""
        # This would contain logic to transform course content into
        # a format that's easily consumable by visualization templates
        structured_data = {
            "main_concept": content.topic,
            "visualization_elements": [],
            "interactive_points": [],
            "explanations": []
        }

        # Process concepts and create visualization elements
        for concept in content.concepts:
            element = self._create_visualization_element(concept)
            structured_data["visualization_elements"].append(element)

        # Process examples and create interactive points
        for example in content.examples:
            point = self._create_interactive_point(example)
            structured_data["interactive_points"].append(point)

        return structured_data

    def _create_visualization_element(self, concept: str) -> Dict:
        """Create a visualization element from a concept"""
        return {
            "type": self._determine_element_type(concept),
            "properties": self._extract_element_properties(concept),
            "animations": self._determine_animations(concept)
        }

    def _create_interactive_point(self, example: Dict) -> Dict:
        """Create an interactive point from an example"""
        return {
            "type": "interactive_point",
            "content": example,
            "interaction_type": self._determine_interaction_type(example)
        }

    def _generate_html(self, template: VisualizationTemplate, content: Dict, params: Optional[Dict]) -> str:
        """Generate HTML content from template"""
        template = self.template_env.get_template(template.html_template)
        return template.render(content=content, params=params or {})

    def _generate_js(self, template: VisualizationTemplate, content: Dict, params: Optional[Dict]) -> str:
        """Generate JavaScript content from template"""
        template = self.template_env.get_template(template.js_template)
        return template.render(content=content, params=params or {})

    def _generate_css(self, template: VisualizationTemplate, content: Dict) -> str:
        """Generate CSS content from template"""
        template = self.template_env.get_template(template.css_template)
        return template.render(content=content)

    def _get_dependencies(self, visualization_type: str) -> list:
        """Get required dependencies for the visualization"""
        common_deps = [
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
            "https://cdnjs.cloudflare.com/ajax/libs/mathjs/9.4.4/math.js"
        ]
        
        # Add visualization-specific dependencies
        specific_deps = {
            "electric_field": ["https://d3js.org/d3.v7.min.js"],
            "circuits": ["https://cdnjs.cloudflare.com/ajax/libs/svg.js/3.1.1/svg.min.js"],
            "ohms_law": ["https://cdn.plot.ly/plotly-latest.min.js"]
        }
        
        return common_deps + specific_deps.get(visualization_type, []) 