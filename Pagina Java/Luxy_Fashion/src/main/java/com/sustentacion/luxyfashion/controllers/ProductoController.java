package com.sustentacion.luxyfashion.controllers;

import com.sustentacion.luxyfashion.models.Producto;
import com.sustentacion.luxyfashion.services.ProductoService;
import com.sustentacion.luxyfashion.services.ProduccionService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

@Controller
@RequestMapping("/admin/producto")
public class ProductoController {

    private final ProductoService productoService;
    private final ProduccionService produccionService;

    public ProductoController(ProductoService productoService, ProduccionService produccionService) {
        this.productoService = productoService;
        this.produccionService = produccionService;
    }

    // ================= LISTAR =================
    @GetMapping
    public String listar(Model model) {

        model.addAttribute("productos", productoService.listaproductoasc());
        model.addAttribute("producto", new Producto());
        model.addAttribute("producciones", produccionService.listar());

        return "admin/producto/indexproducto";
    }

    @GetMapping("/cliente")
    public String listarcliente(Model model) {
        model.addAttribute("productos", productoService.listar());
        model.addAttribute("producto", new Producto());
        model.addAttribute("producciones", produccionService.listar());

        return "cliente/Allproductos";
    }

    // ================= GUARDAR =================
    @PostMapping("/guardar")
    public String guardar(
            @ModelAttribute Producto producto,
            @RequestParam("imagen") MultipartFile imagen
    ) {

        try {
            if (imagen != null && !imagen.isEmpty()) {

                // 📁 carpeta REAL (fuera de resources)
                String carpeta = "uploads/productos/";

                // crear carpeta si no existe
                Files.createDirectories(Paths.get(carpeta));

                // nombre único
                String nombreArchivo = System.currentTimeMillis() + "_" +
                        imagen.getOriginalFilename().replaceAll("\\s+", "");

                // ruta completa
                Path ruta = Paths.get(carpeta + nombreArchivo);

                // guardar imagen
                Files.write(ruta, imagen.getBytes());

                // guardar SOLO el link en BD
                producto.setLink_produc("/uploads/productos/" + nombreArchivo);
            }

            productoService.guardar(producto);

        } catch (Exception e) {
            e.printStackTrace();
        }

        return "redirect:/admin/producto";
    }

    // ================= ELIMINAR =================
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Integer id) {
        productoService.eliminar(id);
        return "redirect:/admin/producto";
    }

    // ================= BUSCAR =================
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

        return "admin/producto/indexproducto";
    }
}
