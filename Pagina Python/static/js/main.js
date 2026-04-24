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

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    const posicionInicial = { x: 0, y: 0.5, z: 6.5 }; 
    camera.position.set(posicionInicial.x, posicionInicial.y, posicionInicial.z);

    const renderer = new THREE.WebGLRenderer({ 
        antialias: true, 
        alpha: true,
        preserveDrawingBuffer: true // Vital para las capturas de pantalla
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

        // Aplicar color inicial si existe el input
        const colorInput = document.getElementById('color-input-global');
        if (colorInput) aplicarColor(colorInput.value);
    });

    // --- 6. LÓGICA DE GUARDADO (VÍA FORMULARIO OCULTO) ---
   // Reemplaza tu función guardarConfiguracion con esta versión optimizada:
// 1. Función para obtener el token real de las cookies del navegador
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

async function guardarConfiguracion() {
    const btnSave = document.getElementById('btn-guardar-3d');
    if (btnSave) {
        btnSave.disabled = true;
        btnSave.innerText = "Guardando...";
    }

    try {
        // Captura de imagen actual (Frente)
        eliminarPrevisualizacion();
        renderer.render(scene, camera);
        const imagenBase64 = renderer.domElement.toDataURL('image/png');

        const datos = {
            'producto_id': document.getElementById('producto-id').value,
            'color': document.getElementById('color-input-global').value,
            'talla': document.getElementById('talla-seleccionada')?.value || 'M',
            'cantidad': 1,
            'estampado_id': idEstampadoSeleccionado,
            'foto_frente': imagenBase64
        };

        const response = await fetch('/inventario/guardar-diseno/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Token real
            },
            body: JSON.stringify(datos)
        });

        if (response.redirected) {
            // Si el servidor nos mandó al login, redirigir manualmente
            window.location.href = response.url;
            return;
        }

        const resultado = await response.json();
        
        if (resultado.status === 'success') {
            alert("¡Producto añadido al carrito!");
            window.location.href = '/ventas/carrito/';
        } else {
            throw new Error(resultado.message);
        }

    } catch (error) {
        console.error("Error:", error);
        alert("Error al guardar: " + error.message);
        if (btnSave) {
            btnSave.disabled = false;
            btnSave.innerText = "Añadir al Carrito";
        }
    }
}

    // --- 7. EVENTOS DE INTERACCIÓN ---

    // Carga de imagen local (Usuario sube su propio logo)
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    idEstampadoSeleccionado = null; 
                    textureLoader.load(event.target.result, (tex) => {
                        tex.colorSpace = THREE.SRGBColorSpace;
                        ultimaTextura = tex;
                    });
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Manejo de la tecla 'A' para estampar
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

    // Movimiento del mouse para previsualizar el decal
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

    // Clic para fijar el estampado
    renderer.domElement.addEventListener('click', () => {
        if (!decalVistaPrevia || !teclaAPresionada) return;
        if (contadorEstampados >= 2) return alert("Máximo 2 estampados permitidos.");
        
        decalVistaPrevia.name = "estampado_fijo";
        decalVistaPrevia.material.opacity = 1.0;
        decalVistaPrevia = null; 
        contadorEstampados++;
    });

    // --- 8. FUNCIONES AUXILIARES (DECAL, COLOR, ETC) ---

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

    // Listener para el input de color
    const colorInputGlobal = document.getElementById('color-input-global');
    if(colorInputGlobal) {
        colorInputGlobal.addEventListener('input', (e) => aplicarColor(e.target.value));
    }

    // Listener para estampados del catálogo
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
    
    async function guardarDiseño() {
    const canvas = document.querySelector('canvas');
    
    // Función para capturar el canvas como Base64 (puedes rotar el modelo entre capturas)
    const imagenFrente = canvas.toDataURL('image/png'); 

    const datos = {
        'producto_id': 9, // O el ID dinámico que tengas
        'color': meshPrenda.material.color.getHexString(),
        'talla': document.getElementById('talla').value,
        'cantidad': 1,
        'foto_frente': imagenFrente, // Enviamos la imagen como texto Base64
    };

    const response = await fetch('/inventario/guardar-diseno/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(datos)
    });

    const resultado = await response.json();
    if (resultado.status === 'success') {
        window.location.href = '/ventas/carrito/';
    }
}

    // Botón de Limpiar
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
            ultimaTextura = null;
            idEstampadoSeleccionado = null;
        };
    }

    // Botón Guardar (conecta con la función del paso 6)
    const btnGuardar = document.getElementById('btn-guardar-3d');
    if (btnGuardar) btnGuardar.onclick = guardarConfiguracion;

    // --- 9. BUCLE DE ANIMACIÓN Y RESIZE ---
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

