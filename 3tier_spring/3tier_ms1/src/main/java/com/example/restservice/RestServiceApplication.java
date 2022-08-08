package com.example.restservice;

import java.util.Arrays;

import org.bson.Document;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;

import kong.unirest.Unirest;

@SpringBootApplication
public class RestServiceApplication  implements ApplicationRunner{
	private static final Logger logger = LoggerFactory.getLogger(RestServiceApplication.class);
	public static Document ms=null;

    public static void main(String[] args) throws Exception {
    	Unirest.config().concurrency(20000, 20000);
		Unirest.config().automaticRetries(false);
		Unirest.config().cacheResponses(false);
		Unirest.config().connectTimeout(0);
		Unirest.config().socketTimeout(0);
		
		//recupero ms2 dal db
		//per il momento lo considero statico poi eventualmente lo devo fare periodicamente
		//per funzionare serve che ms2 viene creato prima di ms1
		MongoClient client = MongoClients.create("mongodb://localhost:27017");
		MongoDatabase sysDb = client.getDatabase("sys");
		MongoCollection<Document> mss = sysDb.getCollection("ms");
		RestServiceApplication.ms = mss.find(Filters.eq("name","ms2")).first();
		client.close();
		
		if(RestServiceApplication.ms == null) {
			throw new Exception("ms ms2 not found");
		}
		
        SpringApplication.run(RestServiceApplication.class, args);
    }
    
    @Override
    public void run(ApplicationArguments args) throws Exception {
    	
    	logger.info("Application started with command-line arguments: {}", Arrays.toString(args.getSourceArgs()));
        logger.info("NonOptionArgs: {}", args.getNonOptionArgs());
        logger.info("OptionNames: {}", args.getOptionNames());

        for (String name : args.getOptionNames()){
        	logger.info("arg-" + name + "=" + args.getOptionValues(name));
        }

        boolean containsOption = args.containsOption("ms.name");
        logger.info("Contains ms.name: " + containsOption);
        logger.info("Contains ms.hw: " + containsOption);
    }

}
