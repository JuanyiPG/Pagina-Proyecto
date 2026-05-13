import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { DecalGeometry } from 'three/addons/geometries/DecalGeometry.js';

/**
 * Módulo de personalización 3D para Luxy Fashion
 */
export function modelo() {
    const container = document.getElementById("container3d");
    if (!container) return;

    // --- 1. CONFIGURACIÓN DE ESCENA Y RENDERER ---
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);
    window.scene = scene; // Exponer la escena globalmente para el conteo

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(0, 0.5, 6.5);

    const renderer = new THREE.WebGLRenderer({ 
        antialias: true, 
        alpha: true,
        preserveDrawingBuffer: true 
    });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
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

    // --- 4. VARIABLES DE ESTADO ---
    let meshCamiseta = [];
    let ultimaTextura = null;
    let decalVistaPrevia = null;
    let teclaAPresionada = false;
    let contadorEstampados = 0;
    let idEstampadoSeleccionado = null; 
    window.listaEstampadosIds = []; // Array global para permitir duplicados en el cobro

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    const textureLoader = new THREE.TextureLoader();

    // --- 5. CARGA DEL MODELO GLB ---
    const loader = new GLTFLoader();
    loader.load('/static/models/t_shirt.glb', (gltf) => {
        const model = gltf.scene;
        model.scale.set(6.0, 6.0, 6.0); 
        scene.add(model);

        // Centrar el modelo
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

        // Aplicar color inicial
        const colorInput = document.getElementById('color-input-global');
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

    // --- 8. EVENTOS DE INTERACCIÓN ---

    // Listener del catálogo
    window.addEventListener('cambioEstampadoManual', (event) => {
        const { url, id } = event.detail;
        idEstampadoSeleccionado = id;
        if (url) {
            textureLoader.load(url, (tex) => {
                tex.colorSpace = THREE.SRGBColorSpace;
                ultimaTextura = tex;
            });
        }
    });

    // Teclado (Tecla A para modo estampado)
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

    // Movimiento del mouse
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
        if (intersects.length > 0) crearDecal(intersects[0], true);
    });

    // Clic para FIJAR estampado
    renderer.domElement.addEventListener('click', () => {
        if (!decalVistaPrevia || !teclaAPresionada) return;
        if (contadorEstampados >= 2) return alert("Máximo 2 estampados permitidos.");
        
        decalVistaPrevia.name = "estampado_fijo";
        decalVistaPrevia.material.opacity = 1.0;
        
        // Guardamos el ID en el array para permitir cobrar repetidos
        if (idEstampadoSeleccionado) {
            window.listaEstampadosIds.push(idEstampadoSeleccionado);
        }

        decalVistaPrevia = null; 
        contadorEstampados++;
    });

    // Botón Limpiar
    const btnLimpiar = document.getElementById('btn-limpiar-estampados');
    if (btnLimpiar) {
        btnLimpiar.onclick = () => {
            const fijos = scene.children.filter(obj => obj.name === "estampado_fijo");
            fijos.forEach(obj => {
                obj.geometry.dispose();
                obj.material.dispose();
                scene.remove(obj);
            });
            window.listaEstampadosIds = [];
            contadorEstampados = 0;
            ultimaTextura = null;
            idEstampadoSeleccionado = null;
        };
    }

// --- 9. LÓGICA DE GUARDADO ---
    async function guardarConfiguracion() {
        console.log("Iniciando proceso de guardado...");

        // Usamos los IDs exactos de tu HTML: 'btn-procesar-guardado' y 'texto-boton'
        const btnSave = document.getElementById('btn-procesar-guardado');
        const textoBtn = document.getElementById('texto-boton');

        if (btnSave) {
            btnSave.disabled = true;
            if (textoBtn) textoBtn.innerText = "Guardando...";
        }

        try {
            // Eliminar la vista previa (el "fantasma") antes de la captura
            eliminarPrevisualizacion();
            
            // Forzar renderizado para obtener la imagen actualizada
            renderer.render(scene, camera);
            const imagenBase64 = renderer.domElement.toDataURL('image/png');
            
            const datos = {
                'producto_id': document.getElementById('producto-id').value,
                'color': document.getElementById('color-input-global').value,
                'talla': document.getElementById('talla-seleccionada')?.value || 'M',
                'cantidad': 1,
                'foto_frente': imagenBase64,
                'cantidad_total_estampados': window.listaEstampadosIds.length, 
                'lista_estampados': window.listaEstampadosIds, 
            };

            const response = await fetch('/inventario/guardar-diseno/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Usamos el token global que definimos en el HTML
                    'X-CSRFToken': window.csrfToken || getCookie('csrftoken'),
                },
                body: JSON.stringify(datos)
            });

            const resultado = await response.json();
            
            if (resultado.status === 'success') {
                console.log("Éxito, redirigiendo...");
                window.location.href = '/ventas/carrito/';
            } else {
                throw new Error(resultado.message || "Error al procesar el diseño.");
            }
        } catch (error) {
            console.error("Error en el guardado:", error);
            alert("Error: " + error.message);
            
            if (btnSave) {
                btnSave.disabled = false;
                if (textoBtn) textoBtn.innerText = "✅ Guardar Diseño";
            }
        }
    }

    // --- IMPORTANTE: VINCULACIÓN DEL EVENTO ---
    const btnEjecutar = document.getElementById('btn-procesar-guardado');
    if (btnEjecutar) {
        btnEjecutar.onclick = (e) => {
            e.preventDefault(); // Evitar cualquier comportamiento por defecto
            guardarConfiguracion();
        };
    }

    // --- 10. BUCLE DE ANIMACIÓN Y RESIZE ---
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