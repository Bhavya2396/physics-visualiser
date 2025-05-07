from fastapi import APIRouter, HTTPException, Body
from typing import Dict, List

from app.services.visualization_generator import VisualizationGenerator
from app.models.visualization import VisualizationRequest, VisualizationResponse, VisualizationError

router = APIRouter()
visualization_generator = VisualizationGenerator()

@router.post(
    "/generate",
    response_model=Dict,
    responses={
        400: {"model": VisualizationError},
        422: {"model": VisualizationError},
        500: {"model": VisualizationError}
    }
)
async def generate_visualization(course_content: Dict = Body(...)):
    """
    Generate visualizations from course content.
    
    The course content should be in the following format:
    {
        "title": "Physics Course Chapter",
        "concepts": [
            {
                "name": "Doppler Effect",
                "description": "The change in frequency of a wave in relation to an observer...",
                "equations": ["f' = f(v ± v_o)/(v ± v_s)"],
                "key_points": [
                    "Frequency increases as source approaches observer",
                    "Frequency decreases as source moves away"
                ]
            }
        ],
        "relationships": [
            {
                "concept1": "frequency",
                "concept2": "velocity",
                "relationship": "proportional"
            }
        ]
    }
    """
    try:
        # Generate visualization using the service
        result = visualization_generator.generate_visualization(course_content)
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating visualization: {str(e)}"
        )

@router.get("/templates")
async def list_templates():
    """List available visualization templates"""
    try:
        templates = {
            "wave": ["doppler-effect", "wave-interference", "standing-waves"],
            "field": ["electric-field", "magnetic-field", "gravitational-field"],
            "circuit": ["series-circuit", "parallel-circuit", "rc-circuit"],
            "motion": ["projectile-motion", "circular-motion", "simple-harmonic-motion"]
        }
        return templates
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching templates: {str(e)}"
        )

@router.get("/preview/{concept_type}/{template_name}")
async def preview_template(concept_type: str, template_name: str):
    """Preview a specific visualization template"""
    try:
        # Generate a sample visualization using the template
        sample_content = _get_sample_content(concept_type, template_name)
        result = visualization_generator.generate_visualization(sample_content)
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating preview: {str(e)}"
        )

def _get_sample_content(concept_type: str, template_name: str) -> Dict:
    """Get sample content for template preview"""
    samples = {
        "wave": {
            "doppler-effect": {
                "title": "Doppler Effect",
                "concepts": [{
                    "name": "Doppler Effect",
                    "type": "wave",
                    "description": "Change in frequency due to relative motion",
                    "equations": ["f' = f(v ± v_o)/(v ± v_s)"],
                    "key_points": [
                        "Frequency increases as source approaches",
                        "Frequency decreases as source recedes"
                    ]
                }]
            }
        },
        "circuit": {
            "rc-circuit": {
                "title": "RC Circuit",
                "concepts": [{
                    "name": "RC Circuit",
                    "type": "circuit",
                    "description": "Charging and discharging of a capacitor through a resistor",
                    "equations": ["V = V₀(1-e^(-t/RC))", "I = I₀e^(-t/RC)"],
                    "key_points": [
                        "Exponential charging curve",
                        "Time constant τ = RC"
                    ]
                }]
            }
        }
    }
    
    if concept_type not in samples or template_name not in samples[concept_type]:
        raise HTTPException(
            status_code=404,
            detail=f"Sample content not found for {concept_type}/{template_name}"
        )
    
    return samples[concept_type][template_name] 