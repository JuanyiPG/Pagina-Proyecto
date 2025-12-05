package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Abono;
import com.sustentacion.luxyfashion.repositories.AbonoRepositories;
import com.sustentacion.luxyfashion.services.AbonoService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;

@Transactional
@Service
public class AbonoServicesImpl implements AbonoService {

    private final AbonoRepositories abonorepositorio;

    public AbonoServicesImpl(AbonoRepositories abonorepositorio) {
        this.abonorepositorio = abonorepositorio;
    }

    @Override
    public Abono guardar(Abono abono) {
        return abonorepositorio.save(abono);
    }

    @Override
    public void eliminar(Integer id) {
        abonorepositorio.deleteById(id);
    }

    @Override
    public List<Abono> listar() {
        return abonorepositorio.findAll();
    }

    @Override
    public List<Abono> findAllByOrderAsc() {
        return abonorepositorio.findAllByOrderByFechaAbonoAsc();
    }

    @Override
    public List<Abono> buscarvarioscampos(String filtro) {
        return abonorepositorio.buscarvarioscampos(filtro);
    }
}
