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
        private Integer id_clien;

        @Column(name = "nom_clien")
        private String nomClien;
        private String dir_clien;
        private String tel_clien;

        @Column(name="correo_clien", unique = true )
        private String correo;

        //@OneToOne(cascade = CascadeType.ALL) //Cascade:relaciona las operaciones en las dos entidades, es decir que trabajan en conjunto.
        // CascadeType.All, es para indicar que todo lo que se opere en esat entidad tambien se ejecute en la otra, en este caso seria Usuario.
        @ManyToOne
        @JoinColumn(name = "id_rol_fk_clien")
        private Rol rol;

    }


