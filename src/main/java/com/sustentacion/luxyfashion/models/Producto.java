package com.sustentacion.luxyfashion.models;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "Producto")
@Setter
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class Producto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String id_produc;
    private String link_produc;
    @Column(name = "nom_produc")
    private String nomProduc;
    private String desc_produc;
    private String categoria_produc;
    private String unid_med_produc;
    private String estado_produc;

    @ManyToOne
    @JoinColumn(name = "id_producc_fk_produc", referencedColumnName = "id_producc")
    private Produccion produccion;


}
