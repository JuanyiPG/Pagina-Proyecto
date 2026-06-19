import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { DecalGeometry } from 'three/addons/geometries/DecalGeometry.js';

/**
 * Módulo de personalización 3D para Luxy Fashion (Adaptado para Cliente y Empleado)
 */
export function modelo(config = {}) {
    // 🔍 CONFIGURACIÓN DINÁMICA DE IDS
    const IDs = {
        container: config.container || "container3d",
        colorInput: config.colorInput || "color-input-global",
        btnLimpiar: config.btnLimpiar || "btn-limpiar-estampados",
        btnGuardar: config.btnGuardar || "btn-procesar-guardado",
        imageInput: config.imageInput || "imageInput",
        getEsclala: config.getEscala || (() => {
            const radio = document.querySelector('input[name="tamano_estam"]:checked');
            return (radio ? parseInt(radio.value) : 100); 
        })
    };

    const container = document.getElementById(IDs.container);
    if (!container) return;

    // --- 1. CONFIGURACIÓN DE ESCENA Y RENDERER ---
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);
    window.scene = scene; 

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(0, 0.5, 6.5);

    const renderer = new THREE.WebGLRenderer({ 
        antialias: true, 
        alpha: true,
        preserveDrawingBuffer: true 
    });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    
    container.innerHTML = "";
    container.appendChild(renderer.domElement);

    // --- 2. ILUMINACIÓN ---
    scene.add(new THREE.AmbientLight(0xffffff, 2.0));
    const lightFront = new THREE.DirectionalLight(0xffffff, 1.5);
    lightFront.position.set(5, 5, 5);
    scene.add(lightFront);

    // --- 3. CONTROLES ---
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.enableZoom = false; 

    // --- 4. VARIABLES DE ESTADO ---
    let meshCamiseta = [];
    let ultimaTextura = null;
    let decalVistaPrevia = null;
    let teclaAPresionada = false;
    let contadorEstampados = 0;
    let idEstampadoSeleccionado = null; 
    window.listaEstampadosIds = []; 
    window.precioExtraTamano = 0;

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    const textureLoader = new THREE.TextureLoader();

    // --- 5. CARGA DEL MODELO GLB ---
    const loader = new GLTFLoader();
    loader.load('/static/models/t_shirt.glb', (gltf) => {
        const model = gltf.scene;
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

        const colorInput = document.getElementById(IDs.colorInput);
        if (colorInput) aplicarColor(colorInput.value);
    });

    // --- 6. FUNCIONES DE AYUDA ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function aplicarColor(hex) {
        meshCamiseta.forEach(m => m.material.color.set(hex));
    }

    function eliminarPrevisualizacion() {
        if (decalVistaPrevia) {
            scene.remove(decalVistaPrevia);
            if (decalVistaPrevia.geometry) decalVistaPrevia.geometry.dispose();
            if (decalVistaPrevia.material) decalVistaPrevia.material.dispose();
            decalVistaPrevia = null;
        }
    }

    // --- 7. LÓGICA DE ESTAMPADO (DECAL) ---
    function crearDecal(hit, esPrevia) {
        const malla = hit.object;
        const posicion = hit.point;
        const normal = hit.face.normal.clone().transformDirection(malla.matrixWorld);

        const material = new THREE.MeshStandardMaterial({
            map: ultimaTextura,
            transparent: true,
            depthWrite: false,
            polygonOffset: true,
            polygonOffsetFactor: -4,
            opacity: esPrevia ? 0.6 : 1.0
        });

        const escalaValor = IDs.getEsclala();
        const size = escalaValor / 100; 
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

    // --- 8. EVENTOS DE INTERACCIÓN ---
    document.querySelectorAll('input[name="tamano_estam"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            const val = e.target.value;
            window.precioExtraTamano = (val === '180') ? 10000 : (val === '100' ? 5000 : 0);
        });
    });

    document.getElementById(IDs.colorInput)?.addEventListener('input', (e) => aplicarColor(e.target.value));

    const imageInputPropio = document.getElementById(IDs.imageInput);
    if (imageInputPropio) {
        imageInputPropio.addEventListener('change', (e) => {
            const archivo = e.target.files[0];
            const errorMsg = document.getElementById('error-message');
            if (archivo) {
                if (archivo.size > 2 * 1024 * 1024) {
                    if (errorMsg) { errorMsg.textContent = "❌ Máximo 2 MB."; errorMsg.style.display = "block"; }
                    e.target.value = ""; return;
                }
                const reader = new FileReader();
                reader.onload = (event) => {
                    textureLoader.load(event.target.result, (tex) => {
                        tex.colorSpace = THREE.SRGBColorSpace;
                        ultimaTextura = tex;
                        idEstampadoSeleccionado = "imagen_propia";
                    });
                };
                reader.readAsDataURL(archivo);
            }
        });
    }

    window.addEventListener('cambioEstampadoManual', (event) => {
        const { url, id } = event.detail;
        idEstampadoSeleccionado = id;
        if (url) {
            textureLoader.load(url, (tex) => {
                tex.colorSpace = THREE.SRGBColorSpace;
                ultimaTextura = tex;
            });
        } else {
            ultimaTextura = null;
            idEstampadoSeleccionado = null;
        }
    });

    window.addEventListener('keydown', (e) => {
        if (e.key.toLowerCase() === 'a') { teclaAPresionada = true; controls.enabled = false; }
    });

    window.addEventListener('keyup', (e) => {
        if (e.key.toLowerCase() === 'a') { teclaAPresionada = false; controls.enabled = true; eliminarPrevisualizacion(); }
    });

    renderer.domElement.addEventListener('mousemove', (event) => {
        if (!ultimaTextura || !teclaAPresionada || contadorEstampados >= 2) { eliminarPrevisualizacion(); return; }
        const rect = renderer.domElement.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(meshCamiseta);
        eliminarPrevisualizacion();
        if (intersects.length > 0) crearDecal(intersects[0], true);
    });

    renderer.domElement.addEventListener('click', () => {
        if (!decalVistaPrevia || !teclaAPresionada || contadorEstampados >= 2) return;
        decalVistaPrevia.name = "estampado_fijo";
        decalVistaPrevia.material.opacity = 1.0;
        if (idEstampadoSeleccionado) window.listaEstampadosIds.push(idEstampadoSeleccionado);
        decalVistaPrevia = null; 
        contadorEstampados++;
    });

    document.getElementById(IDs.btnLimpiar)?.addEventListener('click', () => {
        scene.children.filter(obj => obj.name === "estampado_fijo").forEach(obj => {
            obj.geometry.dispose(); obj.material.dispose(); scene.remove(obj);
        });
        window.listaEstampadosIds = []; contadorEstampados = 0;
    });

    // --- 9. LÓGICA DE GUARDADO CORREGIDA (EMPAQUETADO) ---
    // --- 9. LÓGICA DE GUARDADO CORREGIDA (EMPAQUETADO) ---
    // Busca esta función en main.js y reemplázala por esta versión
async function guardarConfiguracion() {
    const btnSave = document.getElementById(IDs.btnGuardar);
    if (btnSave) btnSave.disabled = true;

    try {
        // Limpiamos la vista previa antes de capturar la imagen
        eliminarPrevisualizacion();
        renderer.render(scene, camera);

        // Construimos el objeto con los datos actuales
        const datos = {
            producto_id: document.getElementById('producto-id')?.value,
            color: document.getElementById(IDs.colorInput)?.value,
            talla: document.querySelector('input[name="talla_m_emp"]:checked')?.value,
            cantidad: parseInt(document.getElementById('input-cantidad-3d')?.value) || 1,
            lista_estampados: window.listaEstampadosIds,
            cantidad_total_estampados: contadorEstampados,
            escala_estampado: IDs.getEsclala() / 100,
            foto_frente: renderer.domElement.toDataURL('image/png')
        };

        // Disparamos el evento hacia el HTML para que la factura lo procese
        window.dispatchEvent(new CustomEvent('disenoGuardadoExitoso', { detail: datos }));
        
    } catch (error) {
        console.error("Error al procesar el guardado:", error);
    } finally {
        if (btnSave) btnSave.disabled = false;
    }
}

    document.getElementById(IDs.btnGuardar)?.addEventListener('click', guardarConfiguracion);

    // --- 10. BUCLE ANIMACIÓN ---
    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();
}