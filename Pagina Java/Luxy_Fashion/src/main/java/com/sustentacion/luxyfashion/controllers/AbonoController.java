package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Abono;
import com.sustentacion.luxyfashion.models.FacturaVenta;
import com.sustentacion.luxyfashion.services.AbonoService;
import com.sustentacion.luxyfashion.services.FacturaVentaService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/abono")
public class AbonoController {

    private final AbonoService abonoService;
    private final FacturaVentaService facturaVentaService;

    public AbonoController(AbonoService abonoService, FacturaVentaService facturaVentaService) {
        this.abonoService = abonoService;
        this.facturaVentaService = facturaVentaService;
    }

    // Mostrar la lista de abonos
    @GetMapping()
    public String listarAbonos(Model model) {
        List<Abono> abonos = abonoService.listar();
        List<FacturaVenta> facturas = facturaVentaService.listar(); // para el select
        model.addAttribute("abonos", abonos);
        model.addAttribute("facturas", facturas);
        model.addAttribute("abono", new Abono()); // para el formulario
        return "admin/listabono/listaAbono"; // tu HTML de listado/registro
    }

    // Guardar un abono
    @PostMapping("/guardar")
    public String guardarAbono(@ModelAttribute("abono") Abono abono,
                               @RequestParam("facturaId") Integer facturaId) {

        FacturaVenta factura = facturaVentaService.buscarPorId(facturaId);

        if (factura != null) {
            abono.setFacturaVenta(factura); // asignar la factura al abono
            abonoService.guardar(abono);    // guardar el abono en la BD
        }

        return "admin/listabono/editarabono";
    }

    // Eliminar un abono
    @GetMapping("/eliminar/{id}")
    public String eliminarAbono(@PathVariable("id") Integer id) {
        abonoService.eliminar(id);
        return "admin/listabono/listaAbono";
    }

    // Buscar abonos (por varios campos)
    @GetMapping("/buscar")
    public String buscarAbonos(@RequestParam(value = "filtro", required = false) String filtro, Model model) {
        List<Abono> abonos;
        if (filtro != null && !filtro.isEmpty()) {
            abonos = abonoService.buscarvarioscampos(filtro);
        } else {
            abonos = abonoService.listar();
        }
        List<FacturaVenta> facturas = facturaVentaService.listar(); // para el select
        model.addAttribute("abonos", abonos);
        model.addAttribute("facturas", facturas);
        model.addAttribute("abono", new Abono());
        return "admin/listabono/listaAbono";
    }
}
