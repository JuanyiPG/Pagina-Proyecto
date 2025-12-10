package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.FacturaCompra;
import com.sustentacion.luxyfashion.models.FacturaVenta;
import com.sustentacion.luxyfashion.services.FacturaCompraService;
import com.sustentacion.luxyfashion.services.EmpleService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/admin/facturacompra")
public class FacturaCompraController {

    private final FacturaCompraService facturaCompraService;
    private final EmpleService empleadoService;

    public FacturaCompraController(FacturaCompraService facturaCompraService,
                                   EmpleService empleadoService) {
        this.facturaCompraService = facturaCompraService;
        this.empleadoService = empleadoService;
    }

    // Listar todas las facturas (con filtro opcional)
    @GetMapping()
    public String listarParaEmpleado(Model model, @RequestParam(required = false) String filtro) {
        List<FacturaCompra> lista;
        if (filtro != null && !filtro.isEmpty()) {
            lista = facturaCompraService.buscarvarioscampos(filtro);
        } else {
            lista = facturaCompraService.listar();
        }
        model.addAttribute("facturas", lista);
        model.addAttribute("facturaCompra", new FacturaCompra());
        model.addAttribute("filtro", filtro);
        return "admin/facturacompra/indexcompra";
    }

    // Mostrar formulario para crear o editar
    @GetMapping("/form")
    public String mostrarFormulario(@RequestParam(required = false) Integer id, Model model) {
        FacturaCompra facturaCompra = (id != null)
                ? facturaCompraService.listar().stream()
                .filter(f -> f.getId_factuc().equals(id))
                .findFirst().orElse(new FacturaCompra())
                : new FacturaCompra();

        model.addAttribute("facturaCompra", facturaCompra);

        // Lista de empleados para el select
        model.addAttribute("empleados", empleadoService.listar());

        return "admin/facturacompra/indexcompra";
    }

    // Guardar o actualizar
    @PostMapping("/guardar")
    public String guardar(@ModelAttribute FacturaCompra facturaCompra) {
        facturaCompraService.guardar(facturaCompra);
        return "redirect:/admin/facturacompra/editarcompra";
    }

    // Eliminar factura
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        facturaCompraService.eliminar(id);
        return "redirect:/admin/facturacompra/indexcompra";
    }

    // Buscar por filtro
    @GetMapping("/buscar")
    public String buscar(@RequestParam String filtro, Model model) {
        List<FacturaCompra> lista = facturaCompraService.buscarvarioscampos(filtro);
        model.addAttribute("facturas", lista);
        model.addAttribute("filtro", filtro);
        return "admin/facturacompra/indexcompra";
    }

    // Mostrar formulario de edición (alias de /form con id)
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {
        return mostrarFormulario(id, model);
    }
}
