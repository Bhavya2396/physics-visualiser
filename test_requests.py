import requests
import json

BASE_URL = "http://localhost:8070"

def test_root():
    """Test the root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print("\n=== Testing Root Endpoint ===")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_wave_visualization():
    """Test wave visualization generation"""
    print("\n=== Testing Wave Visualization ===")
    payload = {
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
    
    response = requests.post(f"{BASE_URL}/api/v1/generate", json=payload)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print("\nGenerated Visualization:")
    print(f"Number of concepts: {result['data']['metadata']['totalConcepts']}")
    print(f"Concept types: {result['data']['metadata']['conceptTypes']}")
    print("\nHTML Preview (first 200 chars):")
    print(result['data']['visualizations'][0]['html'][:200])

def test_field_visualization():
    """Test electric field visualization generation"""
    print("\n=== Testing Field Visualization ===")
    payload = {
        "concepts": [{
            "name": "Electric Field",
            "description": "Region where electric forces act on charged particles",
            "equations": ["E = F/q", "E = k*Q/r²"],
            "key_points": [
                "Field lines point away from positive charges",
                "Field strength decreases with distance squared"
            ]
        }]
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/generate", json=payload)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print("\nGenerated Visualization:")
    print(f"Number of concepts: {result['data']['metadata']['totalConcepts']}")
    print(f"Concept types: {result['data']['metadata']['conceptTypes']}")

def test_available_templates():
    """Test listing available templates"""
    print("\n=== Testing Available Templates ===")
    response = requests.get(f"{BASE_URL}/api/v1/templates")
    print(f"Status Code: {response.status_code}")
    print("Available Templates:")
    print(json.dumps(response.json(), indent=2))

def test_wave_demo():
    """Test the wave demo endpoint"""
    print("\n=== Testing Wave Demo ===")
    response = requests.get(f"{BASE_URL}/demo/wave")
    print(f"Status Code: {response.status_code}")
    print("HTML Content Preview (first 200 chars):")
    print(response.text[:200])

if __name__ == "__main__":
    print("Testing Physics Visualization Service")
    print("=" * 40)
    
    try:
        test_root()
        test_wave_visualization()
        test_field_visualization()
        test_available_templates()
        test_wave_demo()
        
        print("\nAll tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server. Make sure it's running on http://localhost:8070") 