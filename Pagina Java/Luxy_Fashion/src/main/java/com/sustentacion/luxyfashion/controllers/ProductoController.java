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
        model.addAttribute("producciones", produccionService.listar());
        return "admin/producto/indexproducto"; // Cambia al HTML real cuando lo agregues
    }

    // FORMULARIO NUEVO
    @GetMapping("/nuevo")
    public String nuevo(Model model) {
        model.addAttribute("producto", new Producto());
        model.addAttribute("producciones", produccionService.findAllByOrderAsc());
        return "admin/producto/indexproducto";
    }

    @PostMapping("/guardar")
    public String guardar(
            @ModelAttribute Producto producto,
            @RequestParam("imagen") MultipartFile imagen
    ) {

        try {
            if (imagen != null && !imagen.isEmpty()) {

                // 📁 Ruta de la carpeta
                String carpeta = "src/main/resources/static/uploads/productos/";

                // Crear carpeta si no existe
                Files.createDirectories(Paths.get(carpeta));

                // 🖼️ Nombre limpio y único
                String nombreArchivo = System.currentTimeMillis() + "_" +
                        imagen.getOriginalFilename().replaceAll("\\s+", "");

                // 📌 Ruta final
                Path ruta = Paths.get(carpeta + nombreArchivo);

                // 💾 Guardar archivo
                Files.write(ruta, imagen.getBytes());

                // 🔗 Guardar SOLO el link en BD
                producto.setLink_produc("/uploads/productos/" + nombreArchivo);
            }

            productoService.guardar(producto);

        } catch (Exception e) {
            e.printStackTrace();
        }

        return "redirect:/admin/producto";
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