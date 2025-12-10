package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.Abono;
import com.sustentacion.luxyfashion.models.Empleado;
import org.springframework.stereotype.Service;

import java.util.List;

public interface AbonoService {
    Abono guardar(Abono abono);

    void eliminar(Integer id);

    List<Abono> listar();

    List<Abono> findAllByOrderAsc();

    List<Abono> buscarvarioscampos(String filtro);

    Abono buscarPorId(Integer id);
}
