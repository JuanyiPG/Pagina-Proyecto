package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Producto;
import com.sustentacion.luxyfashion.services.ProductoService;
import com.sustentacion.luxyfashion.services.ProduccionService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/admin/producto")
public class  ProductoController {

    private final ProductoService productoService;
    private final ProduccionService produccionService;

    public ProductoController(ProductoService productoService, ProduccionService produccionService) {
        this.productoService = productoService;
        this.produccionService = produccionService;
    }

    // LISTAR
    @GetMapping()
    public String listar(Model model) {
        List<Producto> productos = productoService.listaproductoasc();
        model.addAttribute("productos", productos);
        model.addAttribute("producto", new Producto());
        return "admin/producto/indexproducto"; // Cambia al HTML real cuando lo agregues
    }

    // FORMULARIO NUEVO
    @GetMapping("/nuevo")
    public String nuevo(Model model) {
        model.addAttribute("producto", new Producto());
        model.addAttribute("producciones", produccionService.findAllByOrderAsc());
        return "admin/producto/indexproducto";
    }

    // GUARDAR
    @PostMapping("/guardar")
    public String guardar(@ModelAttribute Producto producto) {
        productoService.guardar(producto);
        return "redirect:/producto";
    }

    // EDITAR
    @GetMapping("/editar/{id}")
    public String editar(@PathVariable Integer id, Model model) {
        Producto producto = productoService.listar()
                .stream()
                .filter(p -> p.getId_produc().equals(id))
                .findFirst()
                .orElseThrow(() -> new RuntimeException("Producto no encontrado"));

        model.addAttribute("producto", producto);
        model.addAttribute("producciones", produccionService.findAllByOrderAsc());
        return "producto/form";
    }

    // ELIMINAR
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        productoService.eliminar(id);
        return "redirect:/producto";
    }

    // BUSCAR
    @GetMapping("/buscar")
    public String buscar(@RequestParam(required = false) String filtro, Model model) {

        List<Producto> productos;

        if (filtro == null || filtro.trim().isEmpty()) {
            productos = productoService.listaproductoasc();
        } else {
            productos = productoService.buscarvarioscampos(filtro);
        }

        model.addAttribute("productos", productos);
        model.addAttribute("filtro", filtro);

        return "admin/producto/indexproducto"; // Cambia al HTML correcto luego
    }
}