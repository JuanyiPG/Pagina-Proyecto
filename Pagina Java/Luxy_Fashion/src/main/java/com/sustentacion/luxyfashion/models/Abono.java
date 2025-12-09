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
@Table(name = "Abono")
@Setter
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class Abono {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_abono;
    @Column(name = "fecha_abono")
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date fechaAbono;
    private BigDecimal monto_abono;
    private String metodo_pago;
    private String descripcion;

    @ManyToOne
    @JoinColumn(name = "id_factuv_fk_abono", referencedColumnName = "id_factuv")
    private FacturaVenta facturaVenta;

}
