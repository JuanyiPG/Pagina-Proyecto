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
@Table(name = "Factura_compra")
@Setter
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class FacturaCompra {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_factuc;
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date fecha_factuc;
    private BigDecimal total;
    private String metodo_pago;
    private String estado;

    @ManyToOne
    @JoinColumn(name = "id_emple_fk", referencedColumnName = "id_emple")
    private Empleado empleado;
}
