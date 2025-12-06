package com.sustentacion.luxyfashion.models;


import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "Det_factv_produc")
@Setter
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class DetFactProducto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_det;
<<<<<<< HEAD
    @Column(name = "desc_det")
=======
    @Column(name="desc_det")
>>>>>>> 61912ab6458c57307b941f5f3c47ebf39652a9bf
    private String descrDet;

    @ManyToOne
    @JoinColumn(name = "id_factuv_fk", referencedColumnName = "id_factuv")
    private FacturaVenta facturaVenta;

    @ManyToOne
    @JoinColumn(name = "id_produc_fk", referencedColumnName = "id_produc")
    private Producto producto;
}
