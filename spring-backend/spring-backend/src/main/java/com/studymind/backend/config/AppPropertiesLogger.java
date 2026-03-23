package com.studymind.backend.config;

import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class AppPropertiesLogger {

    private static final Logger log = LoggerFactory.getLogger(AppPropertiesLogger.class);

    private final String appName;
    private final String aiBaseUrl;

    public AppPropertiesLogger(@Value("${spring.application.name:application}") String appName,
                               @Value("${ai.service.base-url:http://127.0.0.1:5000}") String aiBaseUrl) {
        this.appName = appName;
        this.aiBaseUrl = aiBaseUrl;
    }

    @PostConstruct
    public void logProperties() {
        log.info("Application name (spring.application.name): {}", appName);
        log.info("AI service base URL (ai.service.base-url): {}", aiBaseUrl);
    }
}
