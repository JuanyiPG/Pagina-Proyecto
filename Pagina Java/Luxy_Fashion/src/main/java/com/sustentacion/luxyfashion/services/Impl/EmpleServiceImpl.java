package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.models.Rol;
import com.sustentacion.luxyfashion.models.Usuario;
import com.sustentacion.luxyfashion.repositories.EmpleRepositories;
import com.sustentacion.luxyfashion.repositories.UsuarioRepositories;
import com.sustentacion.luxyfashion.services.EmpleService;
import com.sustentacion.luxyfashion.services.RolService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
@Transactional
public class EmpleServiceImpl implements EmpleService {

    private final EmpleRepositories empleRepositories;
    private final UsuarioRepositories usuarioRepositories;
    private final RolService rolService;

    public EmpleServiceImpl(EmpleRepositories empleRepositories,
                            UsuarioRepositories usuarioRepositories,
                            RolService rolService) {
        this.empleRepositories = empleRepositories;
        this.usuarioRepositories = usuarioRepositories;
        this.rolService = rolService;
    }

    @Override
    public Empleado guardar(Empleado empleado) {
        if (empleRepositories.existsByUsuario(empleado.getUsuario()))
            throw new IllegalArgumentException("Usuario ya en uso");

        if (empleRepositories.existsByCorreo(empleado.getCorreo()))
            throw new IllegalArgumentException("Correo ya registrado");

        Rol rol = rolService.buscarPorNombre("Empleado").get(0);
        empleado.setRol(rol);
        Empleado empleadoGuardado = empleRepositories.save(empleado);

        Usuario usuario = new Usuario();
        usuario.setUsername(empleado.getUsuario());
        usuario.setContrasena(empleado.getContrasena());
        usuario.setRol("EMPLEADO");
        usuario.setEmpleado(empleadoGuardado);
        usuarioRepositories.save(usuario);

        return empleadoGuardado;
    }
@Override
public List<Empleado> listar(){
    return empleRepositories.findAll();
}
@Override
    public List<Empleado> listarEmpleadosOrdenados(){
    return empleRepositories.findAllByOrderByNomEmpleAsc();
    }

    @Override
    public void eliminar(Integer id){
    empleRepositories.deleteById(id);
    }

    @Override
    public Empleado buscarPorId(Integer id){
    return empleRepositories.findById(id).orElse(null);
    }

    @Override
    public List<Empleado>buscarVariosCampos(String filtro){
    return empleRepositories.buscarVariosCampos(filtro);
    }
}
