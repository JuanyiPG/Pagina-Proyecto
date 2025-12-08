package com.sustentacion.luxyfashion.services.Impl;

import com.sustentacion.luxyfashion.models.Abono;
import com.sustentacion.luxyfashion.repositories.AbonoRepositories;
import com.sustentacion.luxyfashion.services.AbonoService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;

@Transactional
@Service
<<<<<<< HEAD:src/main/java/com/sustentacion/luxyfashion/services/Impl/AbonoServiceslmpl.java
public class AbonoServiceslmpl implements AbonoService {
=======
public class AbonoServicesImpl implements AbonoService {
>>>>>>> 61912ab6458c57307b941f5f3c47ebf39652a9bf:src/main/java/com/sustentacion/luxyfashion/services/Impl/AbonoServicesImpl.java

    private final AbonoRepositories abonorepositorio;

<<<<<<< HEAD:src/main/java/com/sustentacion/luxyfashion/services/Impl/AbonoServiceslmpl.java
    public AbonoServiceslmpl(AbonoRepositories abonoRepositories) {
        this.abonoRepositories = abonoRepositories;
=======
    public AbonoServicesImpl(AbonoRepositories abonorepositorio) {
        this.abonorepositorio = abonorepositorio;
>>>>>>> 61912ab6458c57307b941f5f3c47ebf39652a9bf:src/main/java/com/sustentacion/luxyfashion/services/Impl/AbonoServicesImpl.java
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
<<<<<<< HEAD:src/main/java/com/sustentacion/luxyfashion/services/Impl/AbonoServiceslmpl.java
        return abonoRepositories.findAllByOrderByFechaabonoAsc();
=======
        return abonorepositorio.findAllByOrderByFechaAbonoAsc();
>>>>>>> 61912ab6458c57307b941f5f3c47ebf39652a9bf:src/main/java/com/sustentacion/luxyfashion/services/Impl/AbonoServicesImpl.java
    }

    @Override
    public List<Abono> buscarvarioscampos(String filtro) {
<<<<<<< HEAD:src/main/java/com/sustentacion/luxyfashion/services/Impl/AbonoServiceslmpl.java
        return abonoRepositories.buscarVariosCampos(filtro);
    }


    @Transactional
    @Service
    public static class AbonoServiceslmpl implements AbonoService {

        private final AbonoRepositories abonoRepositories;

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
            return abonoRepositories.findAllByOrderByFechaabonoAsc();
        }

        @Override
        public List<Abono> buscarvarioscampos(String filtro) {
            return abonoRepositories.buscarVariosCampos(filtro);
        }


=======
        return abonorepositorio.buscarvarioscampos(filtro);
>>>>>>> 61912ab6458c57307b941f5f3c47ebf39652a9bf:src/main/java/com/sustentacion/luxyfashion/services/Impl/AbonoServicesImpl.java
    }
}
