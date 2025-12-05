package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.DetMateriaPrima;
import com.sustentacion.luxyfashion.models.MateriaPrima;

import java.util.List;

public interface MateriaPrimaService {
    MateriaPrima guardar(MateriaPrima materiaprima);

    DetMateriaPrima guardar(DetMateriaPrima detmateriaprima);

    void eliminar(Integer id);

    List<MateriaPrima> findAllByOrderAsc();

    List<DetMateriaPrima> finAllByOrderAsc();

    List<MateriaPrima> buscarvarioscampos(String filtro);

    List<MateriaPrima> listar();
}
