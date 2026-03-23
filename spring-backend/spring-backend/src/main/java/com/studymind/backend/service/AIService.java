package com.studymind.backend.service;

import com.studymind.backend.model.AIResponse;
import com.studymind.backend.repository.AIRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.stereotype.Service;
import org.springframework.util.MultiValueMap;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientRequestException;
import reactor.core.publisher.Mono;

import java.time.Duration;

@Service
public class AIService {

    private final AIRepository aiRepository;
    private final WebClient webClient;

    public AIService(
            AIRepository aiRepository,
            @Value("${ai.service.base-url:http://127.0.0.1:8000}") String baseUrl
    ) {
        this.aiRepository = aiRepository;
        this.webClient = WebClient.builder()
                .baseUrl(baseUrl)
                .build();
    }

    public String askAI(String question) {
        try {
            String responseBody = webClient.get()
                    .uri(uriBuilder -> uriBuilder
                            .path("/ask")
                            .queryParam("question", question)
                            .build())
                    .retrieve()
                    .bodyToMono(String.class)
                    .block(Duration.ofSeconds(120));

            AIResponse response = new AIResponse(question, responseBody);
            aiRepository.save(response);

            return responseBody;

        } catch (WebClientRequestException ex) {
            return "{\"answer\":\"AI connection error: FastAPI or Ollama is not running.\"}";
        } catch (Exception ex) {
            return "{\"answer\":\"AI service error: " + escapeJson(ex.getMessage()) + "\"}";
        }
    }

    public Mono<String> uploadPDF(MultipartFile file) {
        try {
            MultipartBodyBuilder builder = new MultipartBodyBuilder();
            builder.part("file", file.getResource());

            MultiValueMap<String, org.springframework.http.HttpEntity<?>> multipartData = builder.build();

            return webClient.post()
                    .uri("/upload")
                    .contentType(MediaType.MULTIPART_FORM_DATA)
                    .body(BodyInserters.fromMultipartData(multipartData))
                    .retrieve()
                    .bodyToMono(String.class);

        } catch (Exception ex) {
            return Mono.just("{\"status\":\"Upload failed: " + escapeJson(ex.getMessage()) + "\"}");
        }
    }

    public String getStatus() {
        try {
            return webClient.get()
                    .uri("/status")
                    .retrieve()
                    .bodyToMono(String.class)
                    .block(Duration.ofSeconds(30));
        } catch (Exception ex) {
            return "{\"ready\":false}";
        }
    }

    private String escapeJson(String text) {
        if (text == null) {
            return "";
        }
        return text.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}