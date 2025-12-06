package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.DetMateriaPrima;
import org.springframework.stereotype.Service;

import java.util.List;

public interface DetMateriaPrimaService {
    DetMateriaPrima guardar(DetMateriaPrima detmateriaprima);

    void eliminar(Integer id);

    List<DetMateriaPrima> listar();

    List<DetMateriaPrima> finAllByOrderAsc();

    List<DetMateriaPrima> buscarvarioscampos(String filtro);
}
