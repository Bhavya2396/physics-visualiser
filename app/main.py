from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.services.visualization_generator import VisualizationGenerator

app = FastAPI(
    title="Physics Visualization Service",
    description="Microservice for generating interactive physics visualizations from course content",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize visualization generator
visualization_generator = VisualizationGenerator()

@app.get("/")
async def root():
    """Serve the main HTML interface"""
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/v1/generate")
async def generate_visualization(content: dict = Body(...)):
    """Generate visualization from course content"""
    try:
        result = visualization_generator.generate_visualization(content)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating visualization: {str(e)}"
        )

@app.get("/api/v1/templates")
async def list_templates():
    """List available visualization templates"""
    templates = [
        {
            "id": "wave-doppler",
            "name": "Doppler Effect",
            "category": "wave"
        },
        {
            "id": "wave-interference",
            "name": "Wave Interference",
            "category": "wave"
        },
        {
            "id": "field-electric",
            "name": "Electric Field",
            "category": "field"
        },
        {
            "id": "field-magnetic",
            "name": "Magnetic Field",
            "category": "field"
        },
        {
            "id": "circuit-series",
            "name": "Series Circuit",
            "category": "circuit"
        },
        {
            "id": "circuit-parallel",
            "name": "Parallel Circuit",
            "category": "circuit"
        },
        {
            "id": "motion-projectile",
            "name": "Projectile Motion",
            "category": "motion"
        },
        {
            "id": "motion-circular",
            "name": "Circular Motion",
            "category": "motion"
        }
    ]
    return templates

@app.get("/demo/wave")
async def wave_demo():
    """Demo endpoint for wave visualization"""
    sample_content = {
        "concepts": [{
            "name": "Simple Harmonic Motion",
            "description": "Oscillatory motion that follows a sinusoidal pattern",
            "equations": ["x = A sin(ωt)", "ω = 2πf"],
            "key_points": [
                "Amplitude determines maximum displacement",
                "Frequency determines oscillation rate"
            ]
        }]
    }
    
    result = visualization_generator.generate_visualization(sample_content)
    return HTMLResponse(content=result["data"]["visualizations"][0]["html"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 