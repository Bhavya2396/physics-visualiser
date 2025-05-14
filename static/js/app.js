// Initialize Ace editor
let editor;

document.addEventListener('DOMContentLoaded', function() {
    // Setup Ace editor
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/json");
    editor.setValue(JSON.stringify({
        concept: "",
        parameters: {}
    }, null, 2));

    // Load initial template list
    fetchTemplates();
});

// Fetch available templates from the API
async function fetchTemplates() {
    try {
        const response = await fetch('/api/v1/templates');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const templates = await response.json();
        if (!Array.isArray(templates)) {
            throw new Error('Expected array of templates from server');
        }
        updateTemplateSelect(templates);
    } catch (error) {
        showError('Failed to fetch templates: ' + error.message);
        console.error('Template fetch error:', error);
    }
}

// Update template dropdown with available templates
function updateTemplateSelect(templates) {
    const select = document.getElementById('templateSelect');
    select.innerHTML = '<option value="">Select a template...</option>';
    
    // Group templates by category
    const groupedTemplates = templates.reduce((acc, template) => {
        if (!acc[template.category]) {
            acc[template.category] = [];
        }
        acc[template.category].push(template);
        return acc;
    }, {});

    // Create option groups for each category
    Object.entries(groupedTemplates).forEach(([category, categoryTemplates]) => {
        const optgroup = document.createElement('optgroup');
        optgroup.label = category.charAt(0).toUpperCase() + category.slice(1);
        
        categoryTemplates.forEach(template => {
            const option = document.createElement('option');
            option.value = template.id;
            option.textContent = template.name;
            optgroup.appendChild(option);
        });
        
        select.appendChild(optgroup);
    });
}

// Load template when selected
async function loadSelectedTemplate() {
    const templateId = document.getElementById('templateSelect').value;
    if (!templateId) return;

    try {
        // Extract category and name from template ID
        const [category, type] = templateId.split('-');
        
        // Create template-specific default configuration
        const templateConfig = {
            concept: {
                type: category,
                name: type,
                parameters: getDefaultParameters(category, type)
            }
        };

        editor.setValue(JSON.stringify(templateConfig, null, 2));
    } catch (error) {
        showError('Failed to load template: ' + error.message);
        console.error('Template load error:', error);
    }
}

// Get default parameters based on template type
function getDefaultParameters(category, type) {
    const defaults = {
        wave: {
            doppler: {
                frequency: 440,
                sourceVelocity: 0,
                observerVelocity: 0,
                speedOfSound: 343
            },
            interference: {
                amplitude1: 1,
                amplitude2: 1,
                frequency1: 1,
                frequency2: 1,
                phaseShift: 0
            }
        },
        field: {
            electric: {
                charge: 1,
                position: [0, 0],
                testCharges: 5
            },
            magnetic: {
                current: 1,
                wireLength: 10,
                fieldPoints: 20
            }
        },
        circuit: {
            series: {
                voltage: 12,
                resistors: [100, 200, 300]
            },
            parallel: {
                voltage: 12,
                resistors: [100, 100, 100]
            }
        },
        motion: {
            projectile: {
                initialVelocity: 10,
                angle: 45,
                gravity: 9.81
            },
            circular: {
                radius: 5,
                angularVelocity: 2,
                mass: 1
            }
        }
    };

    return defaults[category]?.[type] || {};
}

// Generate visualization based on JSON input
async function generateVisualization() {
    const visualizationContainer = document.getElementById('visualizationContainer');
    const responseMetadata = document.getElementById('responseMetadata');
    
    try {
        // Parse JSON from editor
        const jsonInput = JSON.parse(editor.getValue());
        
        // Make API request
        const response = await fetch('/api/v1/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonInput)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate visualization');
        }

        const result = await response.json();

        // Display visualization
        visualizationContainer.innerHTML = result.data.visualizations[0].html || 
            '<div class="error-message">No visualization content received</div>';
        
        // Show metadata
        responseMetadata.innerHTML = `
            <div class="success-message">
                <strong>Status:</strong> Success<br>
                <strong>Template:</strong> ${jsonInput.concept.type}-${jsonInput.concept.name}<br>
                <strong>Generation Time:</strong> ${result.metadata?.generationTime || 'N/A'}ms
            </div>
        `;
    } catch (error) {
        showError(error.message);
        console.error('Visualization generation error:', error);
        visualizationContainer.innerHTML = '<div class="error-message">Visualization generation failed</div>';
    }
}

// Load a blank template
function loadTemplate() {
    const blankTemplate = {
        concept: {
            type: "",
            name: "",
            parameters: {}
        }
    };
    editor.setValue(JSON.stringify(blankTemplate, null, 2));
}

// Show error message
function showError(message) {
    const responseMetadata = document.getElementById('responseMetadata');
    responseMetadata.innerHTML = `
        <div class="error-message">
            <strong>Error:</strong> ${message}
        </div>
    `;
} 