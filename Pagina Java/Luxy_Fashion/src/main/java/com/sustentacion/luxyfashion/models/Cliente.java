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

        @OneToOne(mappedBy = "cliente", cascade = CascadeType.ALL)
        private Usuario usuario;

    }


