class WaveVisualization {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        this.frequency = 1;
        this.amplitude = 50;
        this.phase = 0;
        this.animationId = null;
    }

    init() {
        this.setupCanvas();
        this.setupControls();
        this.animate();
    }

    setupCanvas() {
        // Set canvas size based on container
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
        this.width = this.canvas.width;
        this.height = this.canvas.height;
    }

    setupControls() {
        // Add event listeners to controls
        const frequencyControl = document.getElementById('frequency');
        const amplitudeControl = document.getElementById('amplitude');

        if (frequencyControl) {
            frequencyControl.addEventListener('input', (e) => {
                this.frequency = e.target.value / 25;
            });
        }

        if (amplitudeControl) {
            amplitudeControl.addEventListener('input', (e) => {
                this.amplitude = (e.target.value / 100) * (this.height / 4);
            });
        }
    }

    drawWave(time) {
        this.ctx.clearRect(0, 0, this.width, this.height);
        
        this.ctx.beginPath();
        this.ctx.moveTo(0, this.height / 2);
        
        for (let x = 0; x < this.width; x++) {
            const y = this.height / 2 + 
                     this.amplitude * 
                     Math.sin((x / 50) * this.frequency + this.phase);
            this.ctx.lineTo(x, y);
        }
        
        this.ctx.strokeStyle = '#4a9eff';
        this.ctx.lineWidth = 2;
        this.ctx.stroke();
    }

    animate() {
        const animate = (time) => {
            this.phase = time / 1000;
            this.drawWave(time);
            this.animationId = requestAnimationFrame(animate);
        };
        this.animationId = requestAnimationFrame(animate);
    }

    stop() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
}

// Initialize visualization
const visualization = new WaveVisualization('wave-canvas');
visualization.init(); 