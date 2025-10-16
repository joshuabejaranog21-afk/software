package com.agenda.api.controller;

import com.agenda.api.model.Persona;
import com.agenda.api.repository.PersonaRepository;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/personas")
@RequiredArgsConstructor
public class PersonaController {
    
    private final PersonaRepository personaRepository;
    
    /**
     * Crear una nueva persona
     * POST /api/personas
     */
    @PostMapping
    public ResponseEntity<?> crearPersona(@Valid @RequestBody Persona persona) {
        // Verificar si ya existe una persona con este email
        Optional<Persona> existingPersona = personaRepository.findByEmail(persona.getEmail());
        if (existingPersona.isPresent()) {
            return ResponseEntity.badRequest()
                    .body("Ya existe una persona con el email: " + persona.getEmail());
        }
        
        Persona personaGuardada = personaRepository.save(persona);
        return ResponseEntity.status(HttpStatus.CREATED).body(personaGuardada);
    }
    
    /**
     * Obtener todas las personas
     * GET /api/personas
     */
    @GetMapping
    public ResponseEntity<List<Persona>> obtenerTodasLasPersonas() {
        List<Persona> personas = personaRepository.findAll();
        return ResponseEntity.ok(personas);
    }
    
    /**
     * Obtener una persona por ID
     * GET /api/personas/{id}
     */
    @GetMapping("/{id}")
    public ResponseEntity<Persona> obtenerPersonaPorId(@PathVariable Long id) {
        Optional<Persona> persona = personaRepository.findById(id);
        
        if (persona.isPresent()) {
            return ResponseEntity.ok(persona.get());
        } else {
            return ResponseEntity.notFound().build();
        }
    }
    
    /**
     * Actualizar una persona
     * PUT /api/personas/{id}
     */
    @PutMapping("/{id}")
    public ResponseEntity<?> actualizarPersona(@PathVariable Long id, @Valid @RequestBody Persona personaActualizada) {
        Optional<Persona> personaExistente = personaRepository.findById(id);
        
        if (!personaExistente.isPresent()) {
            return ResponseEntity.notFound().build();
        }
        
        Persona persona = personaExistente.get();
        
        // Verificar si el email ya existe en otra persona
        if (!persona.getEmail().equals(personaActualizada.getEmail())) {
            Optional<Persona> personaConEmail = personaRepository.findByEmail(personaActualizada.getEmail());
            if (personaConEmail.isPresent()) {
                return ResponseEntity.badRequest()
                        .body("Ya existe una persona con el email: " + personaActualizada.getEmail());
            }
        }
        
        // Actualizar los campos
        persona.setNombre(personaActualizada.getNombre());
        persona.setApellido(personaActualizada.getApellido());
        persona.setEmail(personaActualizada.getEmail());
        persona.setTelefono(personaActualizada.getTelefono());
        persona.setDireccion(personaActualizada.getDireccion());
        
        Persona personaGuardada = personaRepository.save(persona);
        return ResponseEntity.ok(personaGuardada);
    }
    
    /**
     * Eliminar una persona
     * DELETE /api/personas/{id}
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarPersona(@PathVariable Long id) {
        Optional<Persona> persona = personaRepository.findById(id);
        
        if (!persona.isPresent()) {
            return ResponseEntity.notFound().build();
        }
        
        personaRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}