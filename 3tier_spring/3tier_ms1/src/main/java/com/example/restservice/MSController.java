package com.example.restservice;

import java.net.URI;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import org.apache.commons.math3.distribution.ExponentialDistribution;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import kong.unirest.HttpResponse;
import kong.unirest.JsonNode;
import kong.unirest.Unirest;

@RestController
public class MSController {
	private static final AtomicInteger users = new AtomicInteger(0);

	@Value("${ms.hw}")
	private Float hw;

	@Value("${ms.name}")
	private static String name;

	@Autowired
	private MongoTemplate mt;

	private final Long stime = 200l;

	@GetMapping("/")
	public ResObj ms() {
		// recupero ms1 dal db
		if (RestServiceApplication.ms == null) {
			// recupero ms2 dal db
			Query query = new Query();
			query.addCriteria(Criteria.where("name").is("ms2"));
			RestServiceApplication.ms = this.mt.findOne(query, Ms.class);
		}
		String msAddr = RestServiceApplication.ms.getAddr();
		Integer ms2Port = (Integer) RestServiceApplication.ms.getPrxPort();
		// faccio la richiesta
		String requestedURL = "http://%s:%d%s".formatted(new Object[] { msAddr, ms2Port, "/" });
		CompletableFuture<HttpResponse<JsonNode>> resp = Unirest.get(URI.create(requestedURL).toString()).asJsonAsync();
		this.doWork();
		try {
			resp.get();
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (ExecutionException e) {
			e.printStackTrace();
		}
		return new ResObj();
	}

	@GetMapping("/mnt")
	public ResObj mnt() {
		return new ResObj();
	}

	private void doWork(long stime) {
		ExponentialDistribution dist = new ExponentialDistribution(stime);
		Double isTime = dist.getMean();
		Float d = (float) (isTime.floatValue() * (MSController.users.floatValue() / this.hw));
		MSController.users.incrementAndGet();
		try {
			TimeUnit.MILLISECONDS.sleep(Math.max(Math.round(d), Math.round(isTime)));
		} catch (InterruptedException e) {
			e.printStackTrace();
		}finally {
			MSController.users.decrementAndGet();
		}
	}
	
	private void doWork() {
		this.doWork(this.stime);
	}
	
}
