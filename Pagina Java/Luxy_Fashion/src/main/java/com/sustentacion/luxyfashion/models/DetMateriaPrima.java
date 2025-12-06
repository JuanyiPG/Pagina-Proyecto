package com.sustentacion.luxyfashion.models;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "Det_producc_matp")
@Setter
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class DetMateriaPrima {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_det_pm;
    private String desc_det;

    @ManyToOne
    @JoinColumn(name = "id_matp_fk", referencedColumnName = "id_matp")
    private MateriaPrima materiaPrima;

    @ManyToOne
    @JoinColumn(name = "id_producc_fk", referencedColumnName = "id_producc")
    private Produccion produccion;
}
