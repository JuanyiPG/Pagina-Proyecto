package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.FacturaCompra;
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
@RequestMapping("/admin/facturaventa")
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
        List<FacturaVenta> facturas;

        if (filtro != null && !filtro.isEmpty()) {
            facturas = facturaVentaService.buscarvarioscampos(filtro);
        } else {
            facturas = facturaVentaService.listar();
        }

        model.addAttribute("facturas", facturas);
        model.addAttribute("filtro", filtro);
        model.addAttribute("facturaVenta", new FacturaVenta());
        model.addAttribute("empleados", empleadoService.listar());
        model.addAttribute("clientes", clienteService.listar());
        model.addAttribute("pedidos", pedidoService.listar());

        return "empleado/factventa/indexfacventa";
    }

    @GetMapping("/form")
    public String mostrarFormulario(@RequestParam(required = false) Integer id, Model model) {
        FacturaVenta factura = (id != null)
                ? facturaVentaService.buscarPorId(id)
                : new FacturaVenta();

        model.addAttribute("facturaVenta", factura);
        model.addAttribute("empleados", empleadoService.listar());
        model.addAttribute("clientes", clienteService.listar());
        model.addAttribute("pedidos", pedidoService.listar());

        return "empleado/factventa/indexfacventa"; // Vista específica para el formulario
    }

    @PostMapping("/guardar")
    public String guardar(@ModelAttribute FacturaVenta facturaVenta) {
        facturaVentaService.guardar(facturaVenta);
        return "redirect:/admin/facturaventa?success=true";
    }



    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {

        FacturaVenta facturaVenta = facturaVentaService.buscarPorId(id);

        if (facturaVenta == null) {
            return "redirect:/admin/facturaventa?error=not_found";
        }

        model.addAttribute("facturaVenta", facturaVenta);
        model.addAttribute("empleados", empleadoService.listar());
        model.addAttribute("clientes", clienteService.listar());
        model.addAttribute("pedidos", pedidoService.listar());
        return "empleado/factventa/editarventa";
    }

    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        facturaVentaService.eliminar(id);
        return "redirect:/admin/facturaventa?deleted=true";
    }

    @GetMapping("/buscar")
    public String buscar(@RequestParam(name="buscar", required = false) String filtro, Model model) {
        List<FacturaVenta> facturas;

        if (filtro == null || filtro.isEmpty()) {
            facturas = facturaVentaService.listar();
        } else {
            facturas = facturaVentaService.buscarvarioscampos(filtro);
        }

        model.addAttribute("facturas", facturas);
        model.addAttribute("facturaVenta", new FacturaVenta());
        model.addAttribute("empleados", empleadoService.listar());
        model.addAttribute("clientes", clienteService.listar());
        model.addAttribute("pedidos", pedidoService.listar());
        model.addAttribute("filtro", filtro);

        return "admin/facturaventa/listventa";
    }

    //Vista Admin

    @GetMapping("/lista/admin")
    public String listaradmin(Model model, @RequestParam(required = false) String filtro) {
        List<FacturaVenta> facturas;

        if (filtro != null && !filtro.isEmpty()) {
            facturas = facturaVentaService.buscarvarioscampos(filtro);
        } else {
            facturas = facturaVentaService.listar();
        }

        model.addAttribute("facturas", facturas);
        model.addAttribute("filtro", filtro);
        model.addAttribute("facturaVenta", new FacturaVenta());
        model.addAttribute("empleados", empleadoService.listar());
        model.addAttribute("clientes", clienteService.listar());
        model.addAttribute("pedidos", pedidoService.listar());

        return "admin/facturaventa/listventa";
    }

    @PostMapping("/guardarAdmin")
    public String guardarAdmin(@ModelAttribute FacturaVenta facturaVenta) {
        facturaVentaService.guardar(facturaVenta);
        return "redirect:/admin/facturaventa/lista/admin?success=true";
    }

    @GetMapping("/editarAdmin/{id}")
    public String editarAdmin(@PathVariable Integer id, Model model) {

        FacturaVenta facturaVenta = facturaVentaService.buscarPorId(id);

        if (facturaVenta == null) {
            return "redirect:/admin/facturaventa/lista/admin?error=not_found";
        }

        model.addAttribute("facturaVenta", facturaVenta);
        model.addAttribute("empleados", empleadoService.listar());
        model.addAttribute("clientes", clienteService.listar());
        model.addAttribute("pedidos", pedidoService.listar());
        return "admin/facturaventa/editarventaAdmin";
    }

    @GetMapping("/eliminarAdmin/{id}")
    public String eliminarAdmin(@PathVariable Integer id) {
        facturaVentaService.eliminar(id);
        return "redirect:/admin/facturaventa/lista/admin?deleted=true";
    }

}
