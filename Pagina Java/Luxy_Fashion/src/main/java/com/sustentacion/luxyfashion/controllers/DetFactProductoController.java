package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.DetFactProducto;
import com.sustentacion.luxyfashion.services.DetFactProductoService;
import com.sustentacion.luxyfashion.services.FacturaVentaService;
import com.sustentacion.luxyfashion.services.ProductoService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/admin/detfactproducto")
public class DetFactProductoController {

    private final DetFactProductoService detFactProductoService;
    private final FacturaVentaService facturaVentaService;
    private final ProductoService productoService;

    public DetFactProductoController(DetFactProductoService detFactProductoService,
                                     FacturaVentaService facturaVentaService,
                                     ProductoService productoService) {
        this.detFactProductoService = detFactProductoService;
        this.facturaVentaService = facturaVentaService;
        this.productoService = productoService;
    }

    // Listar todos los detalles (con filtro opcional)
    @GetMapping("/empleado")
    public String listarParaEmpleado(Model model, @RequestParam(required = false) String filtro) {
        List<DetFactProducto> lista;
        if (filtro != null && !filtro.isEmpty()) {
            lista = detFactProductoService.buscarvarioscampos(filtro);
        } else {
            lista = detFactProductoService.listar();
        }
        model.addAttribute("detFactProductos", lista);
        model.addAttribute("filtro", filtro);
        return "empleado/index"; // Ajusta según tu plantilla
    }

    // Mostrar formulario para crear o editar
    @GetMapping("/form")
    public String mostrarFormulario(@RequestParam(required = false) Integer id, Model model) {
        DetFactProducto detFactProducto = (id != null)
                ? detFactProductoService.listar().stream()
                .filter(d -> d.getId_det().equals(id))
                .findFirst().orElse(new DetFactProducto())
                : new DetFactProducto();

        model.addAttribute("detFactProducto", detFactProducto);

        // Listas para selects
        model.addAttribute("facturas", facturaVentaService.listar());
        model.addAttribute("productos", productoService.listar());

        return "empleado/detfactproducto-form";
    }

    // Guardar o actualizar
    @PostMapping("/guardar")
    public String guardar(@ModelAttribute DetFactProducto detFactProducto) {
        detFactProductoService.guardar(detFactProducto);
        return "redirect:/detfactproducto/empleado";
    }

    // Eliminar detalle
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        detFactProductoService.eliminar(id);
        return "redirect:/detfactproducto/empleado";
    }

    // Buscar por filtro
    @GetMapping("/buscar")
    public String buscar(@RequestParam String filtro, Model model) {
        List<DetFactProducto> lista = detFactProductoService.buscarvarioscampos(filtro);
        model.addAttribute("detFactProductos", lista);
        model.addAttribute("filtro", filtro);
        return "empleado/index";
    }

    // Mostrar formulario de edición (alias de /form con id)
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {
        return mostrarFormulario(id, model);
    }
}
