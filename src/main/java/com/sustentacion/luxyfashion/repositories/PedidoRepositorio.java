package com.sustentacion.luxyfashion.repositories;

import com.sustentacion.luxyfashion.models.Empleado;
import com.sustentacion.luxyfashion.models.Pedido;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface PedidoRepositorio extends JpaRepository<Pedido, Integer> {
    List<Pedido> findAllByOrderByNompedAsc();

    @Query("SELECT p FROM Pedido p WHERE " +
            "LOWER(CAST(p.id_pedido AS string)) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(p.link_ped) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(p.Nomped) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(p.talla_ped) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(p.color_ped) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(p.categoria_ped) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(p.material_ped) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(CAST(p.cant_ped AS string)) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(p.desc_ped) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(CAST(p.fecha_ped AS string)) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(CAST(p.subtotal_ped AS string)) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(CAST(p.valor_ped AS string)) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(p.estado_ped) LIKE LOWER(CONCAT('%', :filtro, '%')) OR " +
            "LOWER(CAST(p.cliente AS string)) LIKE LOWER(CONCAT('%', :filtro, '%'))")
    List<Pedido> buscarvarioscampos(@Param("filtro") String filtro);

}
