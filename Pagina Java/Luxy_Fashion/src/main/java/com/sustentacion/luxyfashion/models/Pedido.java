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
@Table(name ="Pedido")
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class Pedido {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_pedido;
    private String link_ped;
    @Column(name= "nom_ped")
    private String nomPed;
    private String talla_ped;
    private String color_ped;
    private String categoria_ped;
    private String material_ped;
    private Integer cant_ped;
    private String desc_ped;
    @DateTimeFormat(pattern = "YYYY/MM/DD")
    private Date fecha_ped;
    private BigDecimal subtotal_ped;
    private BigDecimal valor_ped;
    private String estado_ped;
    private String metodo_pago;

    @ManyToOne
    @JoinColumn(name="id_clien_fk_ped", referencedColumnName = "id_clien")
    private Cliente cliente;

}