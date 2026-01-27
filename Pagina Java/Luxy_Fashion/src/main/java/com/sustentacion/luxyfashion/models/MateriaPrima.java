package com.sustentacion.luxyfashion.models;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;

@Entity
@Table(name = "Materia_prima")
@Setter
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class MateriaPrima {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_matp;
    @Column(name = "nom_matp")
    private String nomMatp;
    private String color_matp;
    private String categoria_matp;
    private String tipo_matp;
    private BigDecimal stock_act_matp;
    private BigDecimal stock_min_matp;
    private String desc_matp;
    private String estado_matp;
}
