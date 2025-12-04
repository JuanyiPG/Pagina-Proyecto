package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Pedido;
import com.sustentacion.luxyfashion.services.PedidoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/pedidos")
public class PedidoController {

    @Autowired
    private PedidoService pedidoService;

    // ============================
    // 1. LISTAR TODOS LOS PEDIDOS
    // ============================
    @GetMapping("")
    public String listarPedidos(Model model){
        List<Pedido> pedidos = pedidoService.listar();
        model.addAttribute("pedidos", pedidos);
        return "pedidos/listar"; // tu archivo listar.html
    }

    // ======================================
    // 2. LISTAR PEDIDOS ORDENADOS POR NOMBRE
    // ======================================
    @GetMapping("/ordenados")
    public String listarPedidosOrdenados(Model model){
        List<Pedido> pedidos = pedidoService.findAllByOrderByNomEmpleAsc();
        model.addAttribute("pedidos", pedidos);
        return "pedidos/listar";
    }

    // ===========================
    // 3. FORMULARIO DE REGISTRO
    // ===========================
    @GetMapping("/nuevo")
    public String NuevoPedido(Model model){
        model.addAttribute("pedido", new Pedido());
        return "pedidos/crear"; // crear.html
    }

    // ===========================
    // 4. GUARDAR PEDIDO
    // ===========================
    @PostMapping("/guardar")
    public String guardarPedido(@ModelAttribute Pedido pedido){
        pedidoService.guardar(pedido);
        return "redirect:/pedidos";
    }

    // ===========================
    // 5. ELIMINAR PEDIDO
    // ===========================
    @GetMapping("/eliminar/{id}")
    public String eliminarPedido(@PathVariable Integer id){
        pedidoService.eliminar(id);
        return "redirect:/pedidos";
    }

    // ===========================
    // 6. BUSCAR POR VARIOS CAMPOS
    // ===========================
    @GetMapping("/buscar")
    public String buscar(@RequestParam("filtro") String filtro, Model model){
        List<Pedido> resultados = pedidoService.buscarVariosCampos(filtro);
        model.addAttribute("pedidos", resultados);
        return "pedidos/listar";
    }
}
