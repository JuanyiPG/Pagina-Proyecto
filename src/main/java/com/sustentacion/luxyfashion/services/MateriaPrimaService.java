package com.sustentacion.luxyfashion.services;

import com.sustentacion.luxyfashion.models.DetMateriaPrima;
import com.sustentacion.luxyfashion.models.MateriaPrima;
import org.springframework.stereotype.Service;

import java.util.List;

public interface MateriaPrimaService {

    MateriaPrima guardar(MateriaPrima materiaprima);

    void eliminar(Integer id);

    List<MateriaPrima> findAllByOrderAsc();

    List<MateriaPrima> buscarvarioscampos(String filtro);

    List<MateriaPrima> listar();
}
