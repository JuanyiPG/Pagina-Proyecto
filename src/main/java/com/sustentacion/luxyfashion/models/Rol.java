package com.sustentacion.luxyfashion.models;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

//Creacion directa entre ka tabla Rol y Java
@Entity //Conexion con la BD
@Table(name = "Rol")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Rol {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_rol;
    private String nom_rol;
    private String desc_rol;

    //Setters
    public void setId_rol(Integer id_rol) {
        this.id_rol = id_rol;
    }

    public void setNom_rol(String nom_rol) {
        this.nom_rol = nom_rol;
    }

    public void setDesc_rol(String desc_rol) {
        this.desc_rol = desc_rol;
    }

    //Getters
    public Integer getId_rol() {
        return id_rol;
    }

    public String getNom_rol() {
        return nom_rol;
    }

    public String getDesc_rol() {
        return desc_rol;
    }
}

