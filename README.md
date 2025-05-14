# Physics Visualization Service

An interactive microservice for generating physics visualizations from course content. This service provides a modern web interface for creating and customizing physics visualizations across various topics including waves, fields, circuits, and motion.

## Features

- **Interactive Web Interface**: Modern, responsive UI with JSON editor
- **Multiple Physics Domains**: Support for various physics concepts
  - Wave phenomena (Doppler effect, interference)
  - Fields (electric, magnetic)
  - Circuits (series, parallel)
  - Motion (projectile, circular)
- **Real-time Visualization**: Instant preview of physics simulations
- **Customizable Parameters**: Adjustable parameters for each visualization type
- **Template System**: Pre-configured templates for common physics scenarios

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Editor**: Ace Editor for JSON configuration
- **Styling**: Bootstrap 5
- **Visualization**: Custom HTML5 Canvas/SVG renderers

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/physics_visualization_service.git
cd physics_visualization_service
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Service

1. Start the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8071
```

2. Open your browser and navigate to:
```
http://localhost:8071
```

## API Endpoints

- `GET /`: Web interface
- `GET /api/v1/templates`: List available visualization templates
- `POST /api/v1/generate`: Generate visualization from content
- `GET /demo/wave`: Wave visualization demo
- `GET /health`: Health check endpoint

## Template Structure

Templates follow this JSON structure:
```json
{
    "concept": {
        "type": "category",
        "name": "template-name",
        "parameters": {
            // template-specific parameters
        }
    }
}
```

### Available Templates

1. Wave Physics
   - Doppler Effect
   - Wave Interference

2. Field Physics
   - Electric Field
   - Magnetic Field

3. Circuit Analysis
   - Series Circuit
   - Parallel Circuit

4. Motion Studies
   - Projectile Motion
   - Circular Motion

## Development

### Project Structure
```
physics_visualization_service/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   └── main.py
├── static/
│   ├── css/
│   ├── js/
│   └── index.html
├── templates/
├── tests/
├── requirements.txt
└── README.md
```

### Adding New Templates

1. Create template configuration in `app/templates`
2. Add template metadata to `app/main.py`
3. Implement visualization logic in `app/services`
4. Add default parameters in `static/js/app.js`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues and feature requests, please create an issue in the GitHub repository. 