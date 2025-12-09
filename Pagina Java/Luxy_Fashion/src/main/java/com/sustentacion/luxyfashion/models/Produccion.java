package com.sustentacion.luxyfashion.models;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;

import java.math.BigDecimal;
import java.util.Date;

@Entity
@Table(name = "Produccion")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Produccion {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_producc;
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date fechaIniProducc;
    private BigDecimal cant_producc;
    private BigDecimal costo_mano_obra_producc;
    private BigDecimal costo_mat_producc;
    private BigDecimal costo_iva_producc;
    private BigDecimal costo_total_producc;
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date fecha_fin_producc;
    private String estado_producc;

    @ManyToOne
    @JoinColumn(name = "id_emple_fk_producc", referencedColumnName = "id_emple")
    private Empleado empleado;

    @ManyToOne
    @JoinColumn(name = "id_pedido_fk_producc", referencedColumnName = "id_pedido")
    private Pedido pedido;

    @ManyToOne
    @JoinColumn(name = " id_matp_fk_producc", referencedColumnName = "id_matp")
    private MateriaPrima materiaPrima;
}
