package com.sustentacion.luxyfashion.models;

import jakarta.persistence.Entity;
import jakarta.persistence.*;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;

import java.math.BigDecimal;
import java.util.Date;

@Entity
@Setter
@Getter
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "Empleado")
public class Empleado {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_emple")
    private Integer idEmple;

    @Column(name = "nom_emple")
    private String nomEmple;
    private String tel_emple;
    @Column(name ="correo_emple")
    private String correo;
    private String dir_emple;
    private String rh_emple;

    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date fecha_naci_emple;

    private String tipo_ident;
    private String num_ident;

    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private Date fecha_ing_emple;

    private BigDecimal salari_emple;
    private String estado_emple;

}

