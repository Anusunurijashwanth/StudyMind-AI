package com.studymind.backend.controller;

import com.studymind.backend.service.AIService;
import org.springframework.http.MediaType;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
        import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/ai")
@CrossOrigin(origins = "*")
public class AIController {

    private final AIService aiService;

    public AIController(AIService aiService) {
        this.aiService = aiService;
    }

    @GetMapping("/ask")
    public String askAI(@RequestParam String question) {
        return aiService.askAI(question);
    }

    @PostMapping(value = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public Mono<String> uploadPDF(@RequestPart("file") MultipartFile file) {
        return aiService.uploadPDF(file);
    }

    @GetMapping("/status")
    public String getStatus() {
        return aiService.getStatus();
    }
}