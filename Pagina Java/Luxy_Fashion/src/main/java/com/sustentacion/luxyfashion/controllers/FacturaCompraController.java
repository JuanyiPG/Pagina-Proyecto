package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.models.FacturaCompra;
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
    private final EmpleService empleService;

    public FacturaCompraController(FacturaCompraService facturaCompraService,
                                   EmpleService empleService) {
        this.facturaCompraService = facturaCompraService;
        this.empleService = empleService;
    }

    // LISTAR
    @GetMapping()
    public String listar(Model model) {
        List<FacturaCompra> facturas = facturaCompraService.listar();
        model.addAttribute("facturas", facturas);
        model.addAttribute("facturaCompra", new FacturaCompra());
        model.addAttribute("empleados", empleService.listar());
        return "admin/facturacompra/indexcompra";
    }

    // NUEVO
    @GetMapping("/nuevo")
    public String nuevo(Model model) {
        model.addAttribute("facturaCompra", new FacturaCompra());
        model.addAttribute("empleados", empleService.listar());
        return "admin/facturacompra/indexcompra";
    }

    // GUARDAR
    @PostMapping("/guardar")
    public String guardar(FacturaCompra facturaCompra) {

        // Asignar empleado correctamente (igual que con Rol en Empleado)
        Integer idEmple = facturaCompra.getEmpleado().getIdEmple();
        Empleado empleado = empleService.buscarPorId(idEmple);
        facturaCompra.setEmpleado(empleado);

        facturaCompraService.guardar(facturaCompra);
        return "redirect:/admin/facturacompra?success=true";
    }

    // EDITAR
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {

        FacturaCompra facturaCompra = facturaCompraService.buscarPorId(id);

        if (facturaCompra == null) {
            return "redirect:/admin/facturacompra?error=not_found";
        }

        model.addAttribute("facturaCompra", facturaCompra);
        model.addAttribute("empleados", empleService.listar());
        return "admin/facturacompra/editarcompra";
    }

    // BUSCAR
    @GetMapping("/buscar")
    public String buscar(
            @RequestParam(name = "buscar", required = false) String filtro,
            Model model) {

        List<FacturaCompra> facturas;

        if (filtro == null || filtro.isEmpty()) {
            facturas = facturaCompraService.listar();
        } else {
            facturas = facturaCompraService.buscarvarioscampos(filtro);
        }

        model.addAttribute("facturas", facturas);
        model.addAttribute("facturaCompra", new FacturaCompra());
        model.addAttribute("empleados", empleService.listar());

        return "admin/facturacompra/indexcompra";
    }

    // ELIMINAR
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        facturaCompraService.eliminar(id);
        return "redirect:/admin/facturacompra?deleted=true";
    }
}

