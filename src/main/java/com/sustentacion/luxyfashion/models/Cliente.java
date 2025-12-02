package com.sustentacion.luxyfashion.models;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "Cliente")
@Setter
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class Cliente {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String id_clien;
    @Column(name = "nom_clien")
    private String nomClie;
    private String dir_clien;
    private String tel_clien;
    private String correo_clien;
    private String usuario_clien;
    private String contra_clien;
    @ManyToOne
    @JoinColumn(name = "id_rol_fk_clien")
    private Rol rol;

}
