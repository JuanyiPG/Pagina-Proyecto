import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { DecalGeometry } from 'three/addons/geometries/DecalGeometry.js';

/**
 * Módulo de personalización 3D para Luxy Fashion (Adaptado para Cliente y Empleado)
 */
export function modelo(config = {}) {

    if (window.personalizador3DInicializado) {
        return;
    }
    window.personalizador3DInicializado = true;

    const IDs = {
        container: config.container || "container3d",
        colorInput: config.colorInput || "color-input-global",
        btnLimpiar: config.btnLimpiar || "btn-limpiar-estampados",
        btnGuardar: config.btnGuardar || "btn-procesar-guardado",
        imageInput: config.imageInput || "imageInput",
        getEscala: config.getEscala || (() => {
            const cuadro = document.querySelector('.cuadro-tamano.activo');
            if (cuadro) {
                return parseInt(cuadro.dataset.scale);
            }
            const radio = document.querySelector(
                'input[name="tamano_estam"]:checked'
            );

            if (radio) {
                return parseInt(radio.value);
            }

            return 40;
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
    window.listaEstampados = [];
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

        const escalaValor = IDs.getEscala();
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
    if (!decalVistaPrevia || !teclaAPresionada || contadorEstampados >= 2) {
        return;
    }

    decalVistaPrevia.name = "estampado_fijo";
    decalVistaPrevia.material.opacity = 1.0;

    if (idEstampadoSeleccionado) {

        const precioImagen =
            idEstampadoSeleccionado === "imagen_propia"
                ? (
                    parseFloat(
                        document.getElementById("precio-imagen-propia")?.value
                    ) || 0
                )
                : 0;

       window.listaEstampados.push({
            id: idEstampadoSeleccionado,
            tipo: idEstampadoSeleccionado === "imagen_propia"
                ? "propio"
                : "catalogo",
            tamano: IDs.getEscala(),
            precio: 0
        });
    }

    decalVistaPrevia = null;
    contadorEstampados++;
});

    document.getElementById(IDs.btnLimpiar)?.addEventListener('click', () => {
        scene.children.filter(obj => obj.name === "estampado_fijo").forEach(obj => {
            obj.geometry.dispose(); obj.material.dispose(); scene.remove(obj);
        });
        window.listaEstampados = []; contadorEstampados = 0;
    });

  // --- 9. LÓGICA DE GUARDADO ---
async function guardarConfiguracion() {

    const btnSave = document.getElementById(IDs.btnGuardar);

    if (btnSave) btnSave.disabled = true;

    try {

        eliminarPrevisualizacion();
        renderer.render(scene, camera);

        console.log("producto-id:", document.getElementById('producto-id'));
        console.log("color:", document.getElementById(IDs.colorInput));
        console.log("talla:", document.querySelector('input[name="talla_personalizada"]:checked'));

        window.listaEstampados.forEach(est => {
            if (est.id === "imagen_propia") {
                est.precio =
                    parseFloat(
                        document.getElementById("precio-imagen-propia")?.value
                    ) || 0;
            }
        });

        const datos = {
            producto_id: document.getElementById('producto-id').value,
            color: document.getElementById(IDs.colorInput).value,
            talla: document.querySelector('input[name="talla_personalizada"]:checked').value,
            cantidad:parseInt(document.getElementById('input-cantidad-3d')?.value) || 1,
            estampado_id: window.listaEstampados.length > 0
                ? window.listaEstampados[0].id
                : null,

            lista_estampados: window.listaEstampados,
            cantidad_total_estampados: contadorEstampados,
            tamano_estampado: IDs.getEscala(),
            foto_frente: renderer.domElement.toDataURL('image/png')
        };
        console.log("CONTADOR:", contadorEstampados);
        console.log("LISTA:", window.listaEstampados);
        const response = await fetch('/inventario/guardar-diseno/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(datos)
        });

        const resultado = await response.json();
        console.log("Respuesta servidor:", resultado);
        console.log("es_empleado:", resultado.es_empleado);
        console.log("Respuesta servidor:", resultado);

        if (resultado.status === 'success') {

            if (resultado.es_empleado) {

                window.dispatchEvent(
                    new CustomEvent('disenoGuardadoExitoso', {
                        detail: {
                            producto_id: resultado.producto_id,
                            precio_unitario: Number(resultado.precio_unitario),
                            precio_final: Number(resultado.precio_final),
                            cantidad: resultado.cantidad,
                            talla: resultado.talla,
                            color: resultado.color,
                            foto_frente: resultado.foto_frente,
                            estampado_id: resultado.estampado_id,
                            tamano_estampado: resultado.tamano_estampado,
                            lista_estampados: resultado.lista_estampados,
                            cantidad_total_estampados:
                                resultado.cantidad_total_estampados
                        }
                    })
                );

            } else {

                window.location.href = "/ventas/carrito/";

            }

        } else {

            alert(resultado.message || "Error al guardar diseño");

        }

    } catch (error) {

        console.error(error);
        alert("Error: " + error.message);

    } finally {

        if (btnSave) btnSave.disabled = false;

    }
}

const btnGuardar = document.getElementById(IDs.btnGuardar);

if (btnGuardar) {
    btnGuardar.onclick = guardarConfiguracion;
}

// --- 10. BUCLE ANIMACIÓN ---
function animate() {

    requestAnimationFrame(animate);

    controls.update();

    renderer.render(scene, camera);
}

animate();

window.reiniciarPersonalizador = function () {
    // Eliminar estampados del modelo
    scene.children
        .filter(obj => obj.name === "estampado_fijo")
        .forEach(obj => {
            obj.geometry.dispose();
            obj.material.dispose();
            scene.remove(obj);
        });

    eliminarPrevisualizacion();

    // Reiniciar variables
    contadorEstampados = 0;
    window.listaEstampados = [];
    ultimaTextura = null;
    idEstampadoSeleccionado = null;

    // Reiniciar color del modelo
    aplicarColor("#ffffff");

    // Reiniciar inputs
    document.getElementById(IDs.colorInput).value = "#ffffff";

    const inputImagen = document.getElementById(IDs.imageInput);
    if (inputImagen) {
        inputImagen.value = "";
    }

    const inputPrecio = document.getElementById("precio-imagen-propia");
    if (inputPrecio) {
        inputPrecio.value = "";
    }

    const inputCantidad = document.getElementById("input-cantidad-3d");
    if (inputCantidad) {
        inputCantidad.value = 1;
    }

    // Seleccionar la primera talla nuevamente
    const primeraTalla = document.querySelector(
        'input[name="talla_personalizada"]'
    );

    if (primeraTalla) {
        primeraTalla.checked = true;
    }
};
}