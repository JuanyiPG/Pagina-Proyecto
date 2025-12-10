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
    @Column(nullable = false)
    private String rol;

    //Conexion de las FK
    @ManyToOne
    @JoinColumn(name = " id_emple_fk_id_usuario", referencedColumnName = "id_emple")
                                                //Para referenciar una columna en concreto
    private Empleado empleado;

    @ManyToOne
    @JoinColumn(name = "id_clien_fk_usuario", referencedColumnName = "id_clien")
    private Cliente cliente;

    public String getRol() {
        return rol;
    }
}
