package com.studymind.backend.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import com.studymind.backend.model.AIResponse;

public interface AIRepository extends MongoRepository<AIResponse, String> {

}