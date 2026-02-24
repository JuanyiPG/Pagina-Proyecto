package com.sustentacion.luxyfashion.config;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.Authentication;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class LoginSuccessHandler implements AuthenticationSuccessHandler {
    public LoginSuccessHandler(){}


    @Override
    public void onAuthenticationSuccess(HttpServletRequest request,
                                        HttpServletResponse response,
                                        Authentication authentication)
                                        throws IOException, ServletException {
        String rol = authentication.getAuthorities()
                .iterator() .next() .getAuthority();
        if (rol.equals("ROLE_ADMIN")) {
            response.sendRedirect("/admin/indexadmin");
        }
        else if (rol.equals("ROLE_CLIENTE"))
        {
            response.sendRedirect("/cliente/indexcliente");
        }
        else if (rol.equals("ROLE_EMPLEADO")) {
            response.sendRedirect("/empleado/indexemple");
        }
        else {
            response.sendRedirect("/");
        }
    }
}