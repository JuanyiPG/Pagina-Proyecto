package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Abono;
import com.sustentacion.luxyfashion.repositories.AbonoRepositories;
import com.sustentacion.luxyfashion.services.AbonoService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;

@Transactional
@Service

public class AbonoServiceslmpl implements AbonoService {
    public final AbonoRepositories abonoRepositories;
    public AbonoServiceslmpl(AbonoRepositories abonoRepositories) {
        this.abonoRepositories = abonoRepositories;
    }

    @Override
    public Abono guardar(Abono abono) {
        return abonoRepositories.save(abono);
    }

    @Override
    public void eliminar(Integer id) {
        abonoRepositories.deleteById(id);
    }

    @Override
    public List<Abono> listar() {
        return abonoRepositories.findAll();
    }

    @Override
    public List<Abono> findAllByOrderAsc() {
        return abonoRepositories.findAllByOrderByFechaAbonoAsc();
    }

    @Override
    public List<Abono> buscarvarioscampos(String filtro) {
        return abonoRepositories.buscarVariosCampos(filtro);
    }

    @Override
    public Abono buscarPorId(Integer id) {
        return abonoRepositories.findById(id).orElse(null);
    }
}
