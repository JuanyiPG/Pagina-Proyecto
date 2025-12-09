package com.sustentacion.luxyfashion.config;

import com.sustentacion.luxyfashion.services.Impl.UsuarioServiceImpl;
import com.sustentacion.luxyfashion.services.UsuarioService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public DaoAuthenticationProvider authenticationProvider(UsuarioServiceImpl userDetailsService) {
        DaoAuthenticationProvider auth = new DaoAuthenticationProvider();
        auth.setUserDetailsService(userDetailsService);
        auth.setPasswordEncoder(passwordEncoder());
        return auth;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .csrf(csrf -> csrf.disable())
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/", "/index", "/login", "/cliente/registrar", "/admin","/empleados").permitAll()
                        .requestMatchers( "/roles/**","/roles/guardar","/roles/eliminar/{id}","/roles/buscar","/roles/editar/{id}").permitAll() //rol
                        .requestMatchers( "/empleado/**").permitAll() //empleado
                        .requestMatchers("/empleado/eliminar/*").permitAll()
                        .requestMatchers("/empleado/editar/*").permitAll()
                        .requestMatchers("/empleado/buscar").permitAll()
                        .requestMatchers("/empleado/guardar").permitAll()
                        .requestMatchers( "/roles","/roles/guardar","/roles/eliminar/{id}","/roles/buscar").permitAll()
                        .requestMatchers("/css/**", "/js/**", "/IMG/**", "/VIDEO/**").permitAll()
                        .requestMatchers("/items/**", "/itemss").permitAll()
                        .requestMatchers("/admin/**").hasRole("ADMIN")
                        .requestMatchers("/amples/**").hasRole("EMPLEADO")
                        .requestMatchers("/cliente/**").hasRole("CLIENTE")
                        .anyRequest().authenticated()
                )
                .formLogin(form -> form
                        .loginPage("/login")
                        .defaultSuccessUrl("/login/default", true)
                        .failureUrl("/login?error=true")
                        .permitAll()
                )
                .logout(logout -> logout
                        .logoutSuccessUrl("/login?logout")
                        .permitAll()
                );

        return http.build();
    }
}

