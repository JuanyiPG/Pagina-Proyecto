package com.sustentacion.luxyfashion.models;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;

@Entity
@Table(name = "Det_factuc_matp")
@Setter
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class DetFactCompra {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_fcm;
    private BigDecimal cant;
    private String desc_det;

    @ManyToOne
    @JoinColumn(name = "id_factuv_fk", referencedColumnName = "id_factuv")
    private FacturaCompra facturaCompra;

    @ManyToOne
    @JoinColumn(name = "id_matp_fk", referencedColumnName = "id_matp")
    private MateriaPrima materiaPrima;
}
