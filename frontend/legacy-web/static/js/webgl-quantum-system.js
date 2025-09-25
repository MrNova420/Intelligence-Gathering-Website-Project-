/**
 * WebGL Quantum Particle System
 * Advanced 3D particle physics engine with quantum entanglement effects
 * Inspired by cutting-edge gaming and enterprise visualization platforms
 */

class WebGLQuantumSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.gl = null;
        this.program = null;
        this.particles = [];
        this.maxParticles = 5000;
        this.quantumFields = [];
        this.entanglementPairs = [];
        this.mousePos = { x: 0, y: 0, z: 0 };
        this.time = 0;
        this.performanceMetrics = {
            fps: 60,
            drawCalls: 0,
            particles: 0
        };
        
        this.init();
    }

    init() {
        this.setupWebGL();
        this.createShaders();
        this.initializeParticles();
        this.setupQuantumFields();
        this.startRenderLoop();
        this.setupEventListeners();
    }

    setupWebGL() {
        this.gl = this.canvas.getContext('webgl2') || this.canvas.getContext('webgl');
        if (!this.gl) {
            console.warn('WebGL not supported, falling back to 2D canvas');
            return this.fallbackTo2D();
        }

        this.gl.enable(this.gl.BLEND);
        this.gl.blendFunc(this.gl.SRC_ALPHA, this.gl.ONE_MINUS_SRC_ALPHA);
        this.gl.enable(this.gl.DEPTH_TEST);
        this.gl.depthFunc(this.gl.LEQUAL);

        this.resizeCanvas();
    }

    createShaders() {
        const vertexShaderSource = `
            attribute vec3 a_position;
            attribute vec3 a_velocity;
            attribute float a_size;
            attribute vec4 a_color;
            attribute float a_quantumState;
            attribute float a_entanglement;
            
            uniform mat4 u_projection;
            uniform mat4 u_view;
            uniform float u_time;
            uniform vec3 u_mousePos;
            uniform vec3 u_quantumField[10];
            
            varying vec4 v_color;
            varying float v_quantumPhase;
            varying float v_distance;
            
            void main() {
                vec3 position = a_position;
                
                // Quantum field interactions
                for(int i = 0; i < 10; i++) {
                    vec3 fieldPos = u_quantumField[i];
                    float dist = distance(position, fieldPos);
                    if(dist < 200.0) {
                        float influence = (200.0 - dist) / 200.0;
                        position += sin(u_time * 0.01 + dist * 0.1) * influence * 5.0 * normalize(fieldPos - position);
                    }
                }
                
                // Mouse interaction with quantum tunneling effect
                float mouseDist = distance(position.xy, u_mousePos.xy);
                if(mouseDist < 150.0) {
                    float mouseInfluence = (150.0 - mouseDist) / 150.0;
                    position.xy += sin(u_time * 0.02 + mouseDist * 0.05) * mouseInfluence * 10.0 * normalize(u_mousePos.xy - position.xy);
                }
                
                // Quantum entanglement oscillation
                position += sin(u_time * 0.003 + a_entanglement * 6.28318) * a_quantumState * 2.0;
                
                gl_Position = u_projection * u_view * vec4(position, 1.0);
                gl_PointSize = a_size * (1.0 + sin(u_time * 0.01 + a_quantumState * 3.14159) * 0.3);
                
                v_color = a_color;
                v_quantumPhase = sin(u_time * 0.005 + a_quantumState * 6.28318) * 0.5 + 0.5;
                v_distance = mouseDist;
            }
        `;

        const fragmentShaderSource = `
            precision mediump float;
            
            varying vec4 v_color;
            varying float v_quantumPhase;
            varying float v_distance;
            
            uniform float u_time;
            
            void main() {
                // Circular particle with quantum glow
                vec2 center = gl_PointCoord - 0.5;
                float dist = length(center);
                
                if(dist > 0.5) {
                    discard;
                }
                
                // Quantum energy visualization
                float energy = 1.0 - dist * 2.0;
                energy = pow(energy, 2.0);
                
                // Quantum phase coloring
                vec3 quantumColor = v_color.rgb;
                quantumColor += vec3(
                    sin(v_quantumPhase * 6.28318) * 0.3,
                    sin(v_quantumPhase * 6.28318 + 2.09439) * 0.3,
                    sin(v_quantumPhase * 6.28318 + 4.18879) * 0.3
                );
                
                // Mouse proximity enhancement
                if(v_distance < 100.0) {
                    float proximity = (100.0 - v_distance) / 100.0;
                    quantumColor += vec3(0.2, 0.4, 0.8) * proximity;
                    energy += proximity * 0.5;
                }
                
                gl_FragColor = vec4(quantumColor, v_color.a * energy * (0.7 + v_quantumPhase * 0.3));
            }
        `;

        this.program = this.createProgram(vertexShaderSource, fragmentShaderSource);
        this.gl.useProgram(this.program);
        this.setupUniforms();
    }

    createProgram(vertexSource, fragmentSource) {
        const vertexShader = this.createShader(this.gl.VERTEX_SHADER, vertexSource);
        const fragmentShader = this.createShader(this.gl.FRAGMENT_SHADER, fragmentSource);
        
        const program = this.gl.createProgram();
        this.gl.attachShader(program, vertexShader);
        this.gl.attachShader(program, fragmentShader);
        this.gl.linkProgram(program);
        
        if (!this.gl.getProgramParameter(program, this.gl.LINK_STATUS)) {
            console.error('Program linking failed:', this.gl.getProgramInfoLog(program));
            return null;
        }
        
        return program;
    }

    createShader(type, source) {
        const shader = this.gl.createShader(type);
        this.gl.shaderSource(shader, source);
        this.gl.compileShader(shader);
        
        if (!this.gl.getShaderParameter(shader, this.gl.COMPILE_STATUS)) {
            console.error('Shader compilation failed:', this.gl.getShaderInfoLog(shader));
            this.gl.deleteShader(shader);
            return null;
        }
        
        return shader;
    }

    setupUniforms() {
        this.uniforms = {
            projection: this.gl.getUniformLocation(this.program, 'u_projection'),
            view: this.gl.getUniformLocation(this.program, 'u_view'),
            time: this.gl.getUniformLocation(this.program, 'u_time'),
            mousePos: this.gl.getUniformLocation(this.program, 'u_mousePos'),
            quantumField: this.gl.getUniformLocation(this.program, 'u_quantumField')
        };

        this.attributes = {
            position: this.gl.getAttribLocation(this.program, 'a_position'),
            velocity: this.gl.getAttribLocation(this.program, 'a_velocity'),
            size: this.gl.getAttribLocation(this.program, 'a_size'),
            color: this.gl.getAttribLocation(this.program, 'a_color'),
            quantumState: this.gl.getAttribLocation(this.program, 'a_quantumState'),
            entanglement: this.gl.getAttribLocation(this.program, 'a_entanglement')
        };
    }

    initializeParticles() {
        this.particles = [];
        this.entanglementPairs = [];
        
        for (let i = 0; i < this.maxParticles; i++) {
            const particle = {
                position: [
                    Math.random() * this.canvas.width - this.canvas.width / 2,
                    Math.random() * this.canvas.height - this.canvas.height / 2,
                    Math.random() * 200 - 100
                ],
                velocity: [
                    (Math.random() - 0.5) * 2,
                    (Math.random() - 0.5) * 2,
                    (Math.random() - 0.5) * 0.5
                ],
                size: Math.random() * 8 + 2,
                color: this.generateQuantumColor(),
                quantumState: Math.random(),
                entanglement: Math.random(),
                life: Math.random() * 1000 + 500,
                maxLife: Math.random() * 1000 + 500,
                energy: Math.random()
            };
            
            this.particles.push(particle);
            
            // Create quantum entanglement pairs
            if (i > 0 && Math.random() < 0.1) {
                this.entanglementPairs.push({
                    particle1: i,
                    particle2: Math.floor(Math.random() * i),
                    strength: Math.random() * 0.5 + 0.5,
                    phase: Math.random() * Math.PI * 2
                });
            }
        }
        
        this.createBuffers();
    }

    generateQuantumColor() {
        const colors = [
            [0.2, 0.8, 1.0, 0.8], // Cyan
            [0.8, 0.2, 1.0, 0.8], // Magenta
            [0.2, 1.0, 0.4, 0.8], // Green
            [1.0, 0.8, 0.2, 0.8], // Orange
            [0.6, 0.2, 0.8, 0.8], // Purple
            [0.8, 0.6, 1.0, 0.8]  // Light Purple
        ];
        
        return colors[Math.floor(Math.random() * colors.length)];
    }

    setupQuantumFields() {
        this.quantumFields = [];
        
        for (let i = 0; i < 10; i++) {
            this.quantumFields.push({
                position: [
                    Math.random() * this.canvas.width - this.canvas.width / 2,
                    Math.random() * this.canvas.height - this.canvas.height / 2,
                    Math.random() * 100 - 50
                ],
                strength: Math.random() * 0.5 + 0.5,
                frequency: Math.random() * 0.02 + 0.01,
                phase: Math.random() * Math.PI * 2
            });
        }
    }

    createBuffers() {
        // Create vertex buffer objects
        this.buffers = {
            position: this.gl.createBuffer(),
            velocity: this.gl.createBuffer(),
            size: this.gl.createBuffer(),
            color: this.gl.createBuffer(),
            quantumState: this.gl.createBuffer(),
            entanglement: this.gl.createBuffer()
        };
    }

    updateParticles() {
        this.time += 16; // Approximate 60fps
        
        for (let i = 0; i < this.particles.length; i++) {
            const particle = this.particles[i];
            
            // Update position based on velocity
            particle.position[0] += particle.velocity[0];
            particle.position[1] += particle.velocity[1];
            particle.position[2] += particle.velocity[2];
            
            // Quantum field interactions
            this.quantumFields.forEach(field => {
                const dx = field.position[0] - particle.position[0];
                const dy = field.position[1] - particle.position[1];
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist < 200) {
                    const influence = (200 - dist) / 200 * field.strength;
                    particle.velocity[0] += Math.sin(this.time * field.frequency + field.phase) * influence * 0.1;
                    particle.velocity[1] += Math.cos(this.time * field.frequency + field.phase) * influence * 0.1;
                }
            });
            
            // Quantum entanglement effects
            this.entanglementPairs.forEach(pair => {
                if (pair.particle1 === i || pair.particle2 === i) {
                    const otherIndex = pair.particle1 === i ? pair.particle2 : pair.particle1;
                    const other = this.particles[otherIndex];
                    
                    if (other) {
                        const entanglementForce = Math.sin(this.time * 0.01 + pair.phase) * pair.strength * 0.01;
                        particle.velocity[0] += (other.position[0] - particle.position[0]) * entanglementForce;
                        particle.velocity[1] += (other.position[1] - particle.position[1]) * entanglementForce;
                    }
                }
            });
            
            // Mouse interaction
            const mouseDx = this.mousePos.x - particle.position[0];
            const mouseDy = this.mousePos.y - particle.position[1];
            const mouseDist = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy);
            
            if (mouseDist < 150) {
                const mouseInfluence = (150 - mouseDist) / 150;
                particle.velocity[0] += mouseDx * mouseInfluence * 0.001;
                particle.velocity[1] += mouseDy * mouseInfluence * 0.001;
            }
            
            // Boundary wrapping
            if (particle.position[0] > this.canvas.width / 2) particle.position[0] = -this.canvas.width / 2;
            if (particle.position[0] < -this.canvas.width / 2) particle.position[0] = this.canvas.width / 2;
            if (particle.position[1] > this.canvas.height / 2) particle.position[1] = -this.canvas.height / 2;
            if (particle.position[1] < -this.canvas.height / 2) particle.position[1] = this.canvas.height / 2;
            
            // Velocity damping
            particle.velocity[0] *= 0.99;
            particle.velocity[1] *= 0.99;
            particle.velocity[2] *= 0.99;
            
            // Life cycle
            particle.life--;
            if (particle.life <= 0) {
                this.resetParticle(particle);
            }
            
            // Update quantum state
            particle.quantumState += 0.01;
            if (particle.quantumState > 1) particle.quantumState = 0;
        }
        
        // Update quantum fields
        this.quantumFields.forEach(field => {
            field.position[0] += Math.sin(this.time * field.frequency) * 0.5;
            field.position[1] += Math.cos(this.time * field.frequency) * 0.5;
        });
    }

    resetParticle(particle) {
        particle.position = [
            Math.random() * this.canvas.width - this.canvas.width / 2,
            Math.random() * this.canvas.height - this.canvas.height / 2,
            Math.random() * 200 - 100
        ];
        particle.velocity = [
            (Math.random() - 0.5) * 2,
            (Math.random() - 0.5) * 2,
            (Math.random() - 0.5) * 0.5
        ];
        particle.life = particle.maxLife;
        particle.color = this.generateQuantumColor();
        particle.quantumState = Math.random();
    }

    render() {
        if (!this.gl || !this.program) return;
        
        this.gl.viewport(0, 0, this.canvas.width, this.canvas.height);
        this.gl.clearColor(0, 0, 0, 0);
        this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);
        
        this.gl.useProgram(this.program);
        
        // Update uniforms
        this.gl.uniform1f(this.uniforms.time, this.time);
        this.gl.uniform3f(this.uniforms.mousePos, this.mousePos.x, this.mousePos.y, this.mousePos.z);
        
        // Update quantum field uniform
        const fieldPositions = new Float32Array(30); // 10 fields * 3 components
        for (let i = 0; i < this.quantumFields.length; i++) {
            fieldPositions[i * 3] = this.quantumFields[i].position[0];
            fieldPositions[i * 3 + 1] = this.quantumFields[i].position[1];
            fieldPositions[i * 3 + 2] = this.quantumFields[i].position[2];
        }
        this.gl.uniform3fv(this.uniforms.quantumField, fieldPositions);
        
        // Set up projection matrix
        const projectionMatrix = this.createOrthographicMatrix(
            -this.canvas.width / 2, this.canvas.width / 2,
            -this.canvas.height / 2, this.canvas.height / 2,
            -200, 200
        );
        this.gl.uniformMatrix4fv(this.uniforms.projection, false, projectionMatrix);
        
        // Set up view matrix (identity for now)
        const viewMatrix = new Float32Array([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        ]);
        this.gl.uniformMatrix4fv(this.uniforms.view, false, viewMatrix);
        
        // Update vertex data
        this.updateVertexData();
        
        // Draw particles
        this.gl.drawArrays(this.gl.POINTS, 0, this.particles.length);
        
        this.performanceMetrics.drawCalls = 1;
        this.performanceMetrics.particles = this.particles.length;
    }

    updateVertexData() {
        const positions = new Float32Array(this.particles.length * 3);
        const velocities = new Float32Array(this.particles.length * 3);
        const sizes = new Float32Array(this.particles.length);
        const colors = new Float32Array(this.particles.length * 4);
        const quantumStates = new Float32Array(this.particles.length);
        const entanglements = new Float32Array(this.particles.length);
        
        for (let i = 0; i < this.particles.length; i++) {
            const p = this.particles[i];
            
            positions[i * 3] = p.position[0];
            positions[i * 3 + 1] = p.position[1];
            positions[i * 3 + 2] = p.position[2];
            
            velocities[i * 3] = p.velocity[0];
            velocities[i * 3 + 1] = p.velocity[1];
            velocities[i * 3 + 2] = p.velocity[2];
            
            sizes[i] = p.size;
            
            colors[i * 4] = p.color[0];
            colors[i * 4 + 1] = p.color[1];
            colors[i * 4 + 2] = p.color[2];
            colors[i * 4 + 3] = p.color[3];
            
            quantumStates[i] = p.quantumState;
            entanglements[i] = p.entanglement;
        }
        
        // Upload data to GPU
        this.uploadBufferData(this.buffers.position, positions, this.attributes.position, 3);
        this.uploadBufferData(this.buffers.velocity, velocities, this.attributes.velocity, 3);
        this.uploadBufferData(this.buffers.size, sizes, this.attributes.size, 1);
        this.uploadBufferData(this.buffers.color, colors, this.attributes.color, 4);
        this.uploadBufferData(this.buffers.quantumState, quantumStates, this.attributes.quantumState, 1);
        this.uploadBufferData(this.buffers.entanglement, entanglements, this.attributes.entanglement, 1);
    }

    uploadBufferData(buffer, data, attribute, size) {
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, buffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, data, this.gl.DYNAMIC_DRAW);
        this.gl.enableVertexAttribArray(attribute);
        this.gl.vertexAttribPointer(attribute, size, this.gl.FLOAT, false, 0, 0);
    }

    createOrthographicMatrix(left, right, bottom, top, near, far) {
        return new Float32Array([
            2 / (right - left), 0, 0, 0,
            0, 2 / (top - bottom), 0, 0,
            0, 0, -2 / (far - near), 0,
            -(right + left) / (right - left), -(top + bottom) / (top - bottom), -(far + near) / (far - near), 1
        ]);
    }

    startRenderLoop() {
        const animate = () => {
            const startTime = performance.now();
            
            this.updateParticles();
            this.render();
            
            const endTime = performance.now();
            const frameTime = endTime - startTime;
            this.performanceMetrics.fps = Math.round(1000 / Math.max(frameTime, 16.67));
            
            requestAnimationFrame(animate);
        };
        
        animate();
    }

    setupEventListeners() {
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mousePos.x = e.clientX - rect.left - this.canvas.width / 2;
            this.mousePos.y = -(e.clientY - rect.top - this.canvas.height / 2);
        });
        
        window.addEventListener('resize', () => {
            this.resizeCanvas();
        });
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        
        if (this.gl) {
            this.gl.viewport(0, 0, this.canvas.width, this.canvas.height);
        }
    }

    fallbackTo2D() {
        // Fallback to 2D canvas for older browsers
        const ctx = this.canvas.getContext('2d');
        console.log('Falling back to 2D quantum system');
        
        const animate2D = () => {
            ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            
            this.particles.forEach(particle => {
                ctx.save();
                ctx.globalAlpha = particle.color[3];
                ctx.fillStyle = `rgb(${particle.color[0] * 255}, ${particle.color[1] * 255}, ${particle.color[2] * 255})`;
                ctx.beginPath();
                ctx.arc(
                    particle.position[0] + this.canvas.width / 2,
                    particle.position[1] + this.canvas.height / 2,
                    particle.size / 2,
                    0,
                    Math.PI * 2
                );
                ctx.fill();
                ctx.restore();
            });
            
            this.updateParticles();
            requestAnimationFrame(animate2D);
        };
        
        animate2D();
    }

    getPerformanceMetrics() {
        return this.performanceMetrics;
    }

    setParticleCount(count) {
        this.maxParticles = Math.min(count, 10000);
        this.initializeParticles();
    }

    addQuantumField(x, y, strength = 1.0) {
        if (this.quantumFields.length < 10) {
            this.quantumFields.push({
                position: [x - this.canvas.width / 2, -(y - this.canvas.height / 2), 0],
                strength: strength,
                frequency: Math.random() * 0.02 + 0.01,
                phase: Math.random() * Math.PI * 2
            });
        }
    }

    destroy() {
        if (this.gl) {
            // Clean up WebGL resources
            Object.values(this.buffers).forEach(buffer => {
                this.gl.deleteBuffer(buffer);
            });
            
            if (this.program) {
                this.gl.deleteProgram(this.program);
            }
        }
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WebGLQuantumSystem;
}

// Global export for browser
if (typeof window !== 'undefined') {
    window.WebGLQuantumSystem = WebGLQuantumSystem;
}