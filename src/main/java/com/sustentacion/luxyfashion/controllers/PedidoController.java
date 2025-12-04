package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Pedido;
import com.sustentacion.luxyfashion.models.Cliente;
import com.sustentacion.luxyfashion.services.PedidoService;
import com.sustentacion.luxyfashion.services.ClienteService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/pedido")
public class PedidoController {

    private final PedidoService pedidoService;
    private final ClienteService clienteService;

    public PedidoController(PedidoService pedidoService, ClienteService clienteService) {
        this.pedidoService = pedidoService;
        this.clienteService = clienteService;
    }

    // ============================
    // LISTAR ORDENADOS (A-Z)
    // ============================
    @GetMapping()
    public String listarOrdenados(Model model) {
        List<Pedido> pedidos = pedidoService.listapedidoasc();
        model.addAttribute("pedidos", pedidos);
        model.addAttribute("pedido", new Pedido());
        model.addAttribute("clientes", clienteService.listar());
        return "pedido/pedido_index";
    }

    // ============================
    // MOSTRAR FORMULARIO NUEVO
    // ============================
    @GetMapping("/nuevo")
    public String nuevo(Model model) {
        model.addAttribute("pedido", new Pedido());
        model.addAttribute("clientes", clienteService.listar());
        return "pedido/pedido_index";
    }

    // ============================
    // GUARDAR PEDIDO
    // ============================
    @PostMapping("/guardar")
    public String guardar(Pedido pedido) {

        // Obtener cliente correctamente
        Cliente clienteSeleccionado = clienteService.buscarPorId(
                pedido.getCliente().getId_clien()
        );
        pedido.setCliente(clienteSeleccionado);

        pedidoService.guardar(pedido);
        return "redirect:/pedido?success=true";
    }

    // ============================
    // EDITAR PEDIDO
    // ============================
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {
        Pedido pedido = pedidoService.buscarPorId(id);

        if (pedido == null) {
            return "redirect:/pedido?error=not_found";
        }

        model.addAttribute("pedido", pedido);
        model.addAttribute("clientes", clienteService.listar());
        return "pedido/editar_pedido";
    }

    // ============================
    // BUSCAR EN TODOS LOS CAMPOS
    // ============================
    @GetMapping("/buscar")
    public String buscar(@RequestParam(name = "buscar", required = false) String filtro,
                         Model model) {

        List<Pedido> pedidos;

        if (filtro == null || filtro.trim().isEmpty()) {
            pedidos = pedidoService.listar();
        } else {
            pedidos = pedidoService.buscarVariosCampos(filtro);
        }

        model.addAttribute("pedidos", pedidos);
        model.addAttribute("pedido", new Pedido());
        model.addAttribute("clientes", clienteService.listar());
        return "pedido/pedido_index";
    }
}
