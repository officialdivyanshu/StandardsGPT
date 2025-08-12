class Starfield {
    constructor() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        this.stars = [];
        this.starCount = 2000;
        this.starSpeed = 0.2;
        this.fov = 500;
        
        this.init();
    }

    init() {
        // Set up renderer
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.domElement.style.position = 'fixed';
        this.renderer.domElement.style.top = 0;
        this.renderer.domElement.style.left = 0;
        this.renderer.domStyle.zIndex = -1;
        document.body.insertBefore(this.renderer.domElement, document.body.firstChild);

        // Set up camera
        this.camera.position.z = 1;
        this.camera.rotation.x = Math.PI / 2;

        // Create starfield
        this.createStarfield();

        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize(), false);

        // Start animation
        this.animate();
    }

    createStarfield() {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        const colors = [];
        const color = new THREE.Color();

        // Create random stars in a sphere
        for (let i = 0; i < this.starCount; i++) {
            // Position stars in a sphere
            const radius = 1000;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            
            const x = radius * Math.sin(phi) * Math.cos(theta);
            const y = radius * Math.sin(phi) * Math.sin(theta);
            const z = radius * Math.cos(phi);
            
            vertices.push(x, y, z);
            
            // Add some color variation
            const hue = 0.1 + Math.random() * 0.2; // Yellowish to white
            const saturation = 0.2 + Math.random() * 0.3; // Slightly desaturated
            const lightness = 0.5 + Math.random() * 0.5; // Bright stars
            color.setHSL(hue, saturation, lightness);
            colors.push(color.r, color.g, color.b);
            
            // Store star data for animation
            this.stars.push({
                x: x,
                y: y,
                z: z,
                speed: 0.5 + Math.random() * this.starSpeed
            });
        }

        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 1.2,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            sizeAttenuation: true,
            blending: THREE.AdditiveBlending
        });

        this.starField = new THREE.Points(geometry, material);
        this.scene.add(this.starField);
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        this.updateStars();
        this.renderer.render(this.scene, this.camera);
    }

    updateStars() {
        const positions = this.starField.geometry.attributes.position.array;
        
        for (let i = 0; i < positions.length; i += 3) {
            const star = this.stars[i / 3];
            
            // Move stars toward camera (simplified 3D movement)
            positions[i + 2] -= star.speed;
            
            // Reset stars that are too close
            if (positions[i + 2] < -this.fov) {
                positions[i + 2] = this.fov;
            }
        }
        
        this.starField.geometry.attributes.position.needsUpdate = true;
        
        // Add subtle rotation for more dynamic feel
        this.starField.rotation.z += 0.0001;
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// Initialize the starfield when the page loads
window.addEventListener('load', () => {
    const starfield = new Starfield();
});
