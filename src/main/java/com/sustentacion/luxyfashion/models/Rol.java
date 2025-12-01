package com.sustentacion.luxyfashion.models;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
//El model es un OBJETO en su totalidad, ya que se usa en todas las capas, siendo la principal referencia dentro del proyecto.
//Creacion directa entre la tabla Rol y Java
@Entity //Conexion con la BD, se guarda en la BD.
@Table(name = "Rol")
@Getter
@Setter
//Para colocar un constructor vacio.
@NoArgsConstructor
@AllArgsConstructor
public class Rol {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) //Genera el ID automaticamente
    private Integer id_rol;
    @Column(name = "nom_rol")
    private String nomRol;
    private String desc_rol;

}

