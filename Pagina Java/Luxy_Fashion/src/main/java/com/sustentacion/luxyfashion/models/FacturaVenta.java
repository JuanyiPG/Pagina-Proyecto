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
@Table(name="Factura_venta")
@Setter
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class FacturaVenta {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_factuv;
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date fechafactuv;
    private BigDecimal subtotal_factuv;
    @Column(name = "fecha_factuv")
    private BigDecimal iva_factuv;
    private BigDecimal total_factuv;
    @Column(name = "metodo_pago_factuv")
    private String metodo_pago;
    private BigDecimal descu_factuv;
    private String estado_factuv;

    @ManyToOne
    @JoinColumn(name = "id_emple_fk_factuv", referencedColumnName = "id_emple")
    private Empleado empleado;

    @ManyToOne
    @JoinColumn(name = "id_clien_fk_factuv", referencedColumnName = "id_clien")
    private Cliente cliente;

    @ManyToOne
    @JoinColumn(name = "id_pedido_fk_factuv", referencedColumnName = "id_pedido")
    private Pedido pedido;
}
