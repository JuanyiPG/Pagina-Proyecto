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
    private String color;
    private String categoria;
    private String tipo;
    private BigDecimal stock_act;
    private BigDecimal stock_min;
    private String desc_matp;
    private String estado;
}
