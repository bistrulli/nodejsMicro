package com.example.restservice;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface MSRepository extends MongoRepository < MSModel, Long > {
	
	@Query("{name:'?0'}")
    MSModel findItemByName(String name);
}