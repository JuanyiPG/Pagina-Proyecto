import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { DecalGeometry } from 'three/addons/geometries/DecalGeometry.js';

export function modelo() {
    const container = document.getElementById("container3d");
    if (!container) return;

    // --- CONFIGURACIÓN DE ESCENA ---
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    const posicionInicial = { x: 0, y: 0.5, z: 6.5 }; 
    camera.position.set(posicionInicial.x, posicionInicial.y, posicionInicial.z);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // --- LUCES ---
    scene.add(new THREE.AmbientLight(0xffffff, 2.0));
    const lightFront = new THREE.DirectionalLight(0xffffff, 1.5);
    lightFront.position.set(5, 5, 5);
    scene.add(lightFront);

    // --- CONTROLES DE CÁMARA ---
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // --- VARIABLES DE ESTADO ---
    let meshCamiseta = [];
    let ultimaTextura = null;
    let decalVistaPrevia = null;
    let teclaAPresionada = false;
    let contadorEstampados = 0;

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    const textureLoader = new THREE.TextureLoader();

    // --- CARGA DEL MODELO (t_shirt.glb) ---
    const loader = new GLTFLoader();
    loader.load('/static/models/t_shirt.glb', (gltf) => {
        const model = gltf.scene;
        
        // DISMINUCIÓN DEL MODELO (de 7.5 a 6.0)
        model.scale.set(6.0, 6.0, 6.0); 
        scene.add(model);

        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        model.position.sub(center);

        model.traverse((child) => {
            if (child.isMesh) {
                meshCamiseta.push(child);
                child.material = new THREE.MeshStandardMaterial({
                    color: 0xffffff,
                    roughness: 0.7,
                    metalness: 0.1,
                    side: THREE.DoubleSide
                });
            }
        });

        // Color inicial si existe el input
        const colorInput = document.getElementById('color-input-global');
        if (colorInput) aplicarColor(colorInput.value);
    });

    // --- LÓGICA DE TECLADO---
    window.addEventListener('keydown', (e) => {
        if (e.key.toLowerCase() === 'a') {
            teclaAPresionada = true;
            controls.enabled = false; 
        }
    });

    window.addEventListener('keyup', (e) => {
        if (e.key.toLowerCase() === 'a') {
            teclaAPresionada = false;
            controls.enabled = true; 
            eliminarPrevisualizacion();
        }
    });

    // --- MOVIMIENTO PARA PREVISUALIZAR ---
    renderer.domElement.addEventListener('mousemove', (event) => {
        if (!ultimaTextura || !teclaAPresionada || contadorEstampados >= 2) {
            eliminarPrevisualizacion();
            return;
        }

        const rect = renderer.domElement.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(meshCamiseta);

        eliminarPrevisualizacion();
        if (intersects.length > 0) {
            crearDecal(intersects[0], true);
        }
    });

    // --- CLIC PARA FIJAR EL ESTAMPADO ---
    renderer.domElement.addEventListener('click', () => {
        if (!decalVistaPrevia || !teclaAPresionada) return;
        if (contadorEstampados >= 2) {
            alert("Límite de 2 estampados alcanzado.");
            return;
        }
        
        decalVistaPrevia.name = "estampado_fijo";
        decalVistaPrevia.material.opacity = 1.0;
        decalVistaPrevia = null; 
        contadorEstampados++;
    });

    // --- MOTOR DE DECAL (ESTAMPADOS) ---
    function crearDecal(hit, esPrevia) {
        const malla = hit.object;
        const posicion = hit.point;
        const normal = hit.face.normal.clone().transformDirection(malla.matrixWorld);

        const material = new THREE.MeshStandardMaterial({
            map: ultimaTextura,
            transparent: true,
            depthTest: true,
            depthWrite: false,
            polygonOffset: true,
            polygonOffsetFactor: -4,
            opacity: esPrevia ? 0.6 : 1.0
        });

        const slider = document.getElementById('sizeSlider');
        const size = (slider ? parseInt(slider.value) : 60) / 50; 
        const dimensiones = new THREE.Vector3(size, size, 1.0);

        const m = new THREE.Matrix4();
        m.lookAt(normal, new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 1, 0));
        const orientacion = new THREE.Euler().setFromRotationMatrix(m);

        const decalGeom = new DecalGeometry(malla, posicion, orientacion, dimensiones);
        const decalMesh = new THREE.Mesh(decalGeom, material);

        decalMesh.name = esPrevia ? "vista_previa" : "estampado_fijo";
        scene.add(decalMesh);
        if (esPrevia) decalVistaPrevia = decalMesh;
    }

    // --- LIMPIAR TODO ---
    const btnLimpiar = document.getElementById('btn-limpiar-estampados');
    if (btnLimpiar) {
        btnLimpiar.onclick = () => {
            const fijos = scene.children.filter(obj => obj.name === "estampado_fijo");
            fijos.forEach(obj => {
                obj.geometry.dispose();
                obj.material.dispose();
                scene.remove(obj);
            });
            contadorEstampados = 0;
            eliminarPrevisualizacion();
        };
    }

    // --- UTILIDADES ---
    function eliminarPrevisualizacion() {
        if (decalVistaPrevia) {
            decalVistaPrevia.geometry.dispose();
            decalVistaPrevia.material.dispose();
            scene.remove(decalVistaPrevia);
            decalVistaPrevia = null;
        }
    }

    function aplicarColor(hex) {
        meshCamiseta.forEach(m => m.material.color.set(hex));
    }

    // --- EVENTOS DE INTERFAZ ---
    document.getElementById('imageInput').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (ev) => {
                textureLoader.load(ev.target.result, (tex) => {
                    tex.colorSpace = THREE.SRGBColorSpace;
                    ultimaTextura = tex;
                });
            };
            reader.readAsDataURL(file);
        }
    });

    document.getElementById('color-input-global').addEventListener('input', (e) => {
        aplicarColor(e.target.value);
    });

    // ESCUCHA PARA EL CATÁLOGO (EVENTO PERSONALIZADO)
    window.addEventListener('cambioEstampadoManual', (event) => {
        const urlImagen = event.detail;
        textureLoader.load(urlImagen, (tex) => {
            tex.colorSpace = THREE.SRGBColorSpace;
            ultimaTextura = tex;
        });
    });

    // --- CICLO DE ANIMACIÓN ---
    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
}