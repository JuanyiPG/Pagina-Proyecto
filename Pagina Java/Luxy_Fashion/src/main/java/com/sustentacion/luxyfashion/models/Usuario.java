package com.sustentacion.luxyfashion.models;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "usuarios")
@Setter
@Getter
@AllArgsConstructor
@NoArgsConstructor
public class Usuario {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_usuario;

    @Column(unique = true, nullable = false)
    private String username;

    @Column(nullable = false)
    private String contrasena;

    //Conexion de las FK
    @ManyToOne(optional = true)
    @JoinColumn(name = "id_emple_fk_usuario", referencedColumnName = "id_emple")
                                                //Para referenciar una columna en concreto
    private Empleado empleado;

    @ManyToOne(optional = true)
    @JoinColumn(name = "id_clien_fk_usuario")
    private Cliente cliente;

}
