package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.FacturaVenta;
import com.sustentacion.luxyfashion.services.FacturaVentaService;
import com.sustentacion.luxyfashion.services.EmpleService;
import com.sustentacion.luxyfashion.services.ClienteService;
import com.sustentacion.luxyfashion.services.PedidoService;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/facturaventa")
public class FacturaVentaController {

    private final FacturaVentaService facturaVentaService;
    private final EmpleService empleadoService;
    private final ClienteService clienteService;
    private final PedidoService pedidoService;

    public FacturaVentaController(FacturaVentaService facturaVentaService,
                                  EmpleService empleadoService,
                                  ClienteService clienteService,
                                  PedidoService pedidoService) {
        this.facturaVentaService = facturaVentaService;
        this.empleadoService = empleadoService;
        this.clienteService = clienteService;
        this.pedidoService = pedidoService;
    }

    @GetMapping()
    public String listar(Model model, @RequestParam(required = false) String filtro) {

        List<FacturaVenta> lista;

        if (filtro != null && !filtro.isEmpty()) {
            lista = facturaVentaService.buscarvarioscampos(filtro);
        } else {
            lista = facturaVentaService.listar();
        }

        model.addAttribute("facturas", lista);
        model.addAttribute("filtro", filtro);

        return "admin/facturaventa/listventa"; // Ajusta según tu HTML
    }

    // ===========================
    // FORMULARIO CREAR / EDITAR
    // ===========================
    @GetMapping("/form")
    public String mostrarFormulario(@RequestParam(required = false) Integer id, Model model) {

        FacturaVenta factura = (id != null)
                ? facturaVentaService.buscarPorId(id)
                : new FacturaVenta();

        model.addAttribute("facturaVenta", factura);

        // Selects
        model.addAttribute("empleados", empleadoService.listar());
        model.addAttribute("clientes", clienteService.listar());
        model.addAttribute("pedidos", pedidoService.listar());

        return "admin/facturaventa/listventa";
    }

    // GUARDAR

    @PostMapping("/guardar")
    public String guardar(@ModelAttribute FacturaVenta facturaVenta) {
        facturaVentaService.guardar(facturaVenta);
        return "redirect:/admin/facturaventa/editarventa";
    }


    // ELIMINAR
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        facturaVentaService.eliminar(id);
        return "redirect:/admin/facturaventa/listventa";
    }

    // EDITAR
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {
        return mostrarFormulario(id, model);
    }

    // BUSCAR
    @GetMapping("/buscar")
    public String buscar(@RequestParam String filtro, Model model) {
        List<FacturaVenta> lista = facturaVentaService.buscarvarioscampos(filtro);

        model.addAttribute("facturas", lista);
        model.addAttribute("filtro", filtro);

        return "admin/facturaventa/listventa";
    }
}
