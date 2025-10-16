package com.agenda.api.repository;

import com.agenda.api.model.Persona;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PersonaRepository extends JpaRepository<Persona, Long> {
    
    /**
     * Busca una persona por su email
     * @param email el email de la persona
     * @return Optional con la persona si existe, empty si no existe
     */
    Optional<Persona> findByEmail(String email);
}