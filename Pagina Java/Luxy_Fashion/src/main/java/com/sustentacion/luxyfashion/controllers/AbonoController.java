package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Abono;
import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.models.FacturaVenta;
import com.sustentacion.luxyfashion.models.Pedido;
import com.sustentacion.luxyfashion.services.AbonoService;
import com.sustentacion.luxyfashion.services.FacturaVentaService;
import com.sustentacion.luxyfashion.services.PedidoService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/admin/indexadmin/abono")
public class AbonoController {

    private final AbonoService abonoService;
    private final PedidoService pedidoService;

    public AbonoController(AbonoService abonoService, PedidoService pedidoService) {
        this.abonoService = abonoService;
        this.pedidoService = pedidoService;
    }

    // Mostrar la lista de abonos
    @GetMapping()
    public String listarAbonos(Model model) {
        List<Abono> abonos = abonoService.listar();
        List<Pedido> pedidos = pedidoService.listar(); // para el select
        model.addAttribute("abonos", abonos);
        model.addAttribute("pedidos", pedidos);
        model.addAttribute("abono", new Abono()); // para el formulario
        return "cliente/abono"; // tu HTML de listado/registro
    }

    @GetMapping("/lista/admin")
    public String listarAdmin(Model model) {
        List<Abono> abonos = abonoService.listar();
        List<Pedido> pedidos = pedidoService.listar(); // para el select
        model.addAttribute("abonos", abonos);
        model.addAttribute("pedidos", pedidos);
        model.addAttribute("abono", new Abono()); // para el formulario
        return "admin/listabono/abono"; // tu HTML de listado/registro
    }

    @GetMapping("/lista/emple")
    public String listarEmple(Model model) {
        List<Abono> abonos = abonoService.listar();
        List<Pedido> pedidos = pedidoService.listar(); // para el select
        model.addAttribute("abonos", abonos);
        model.addAttribute("pedidos", pedidos);
        model.addAttribute("abono", new Abono()); // para el formulario
        return "empleado/listabono/abono"; // tu HTML de listado/registro
    }

    // Guardar un abono
    @PostMapping("/guardar")
    public String guardarAbono(@ModelAttribute Abono abono) {
        abonoService.guardar(abono);
        return "redirect:/pedido/confirmacion";
    }

    // Eliminar un abono
    @GetMapping("/eliminar/{id}")
    public String eliminarAbono(@PathVariable("id") Integer id) {
        abonoService.eliminar(id);
        return "redirect:empleado?success=true";
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
        List<Pedido> pedidos = pedidoService.listar();// para el select
        model.addAttribute("abonos", abonos);
        model.addAttribute("pedidos", pedidos);
        model.addAttribute("abono", new Abono());
        return "cliente/abono";
    }

    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model){
        Abono abono = abonoService.buscarPorId(id);
        if (abono == null){
            return "redirect:/empleado?error=not_found";
        }
        model.addAttribute("abono", abono);
        return "admin/empleado/editar_emple";
    }

    @GetMapping("/abono/nuevo/{idPedido}")
    public String nuevoAbono(@PathVariable Integer idPedido, Model model) {

        Pedido pedido = pedidoService.buscarPorId(idPedido);

        Abono abono = new Abono();
        abono.setPedido(pedido);

        model.addAttribute("abono", abono);
        model.addAttribute("pedido", pedido);

        return "cliente/abono";
    }

}
