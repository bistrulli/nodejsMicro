package com.example.restservice;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import org.apache.commons.math3.distribution.ExponentialDistribution;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MSController {
	private static final AtomicInteger users = new AtomicInteger(0);

	@Value("${ms.hw}")
	private Float hw;

	@Value("${ms.name}")
	private String name;

	private final Long stime = 60l;

	@GetMapping("/")
	public ResObj ms() {
		this.doWork();
		return new ResObj();
	}

	@GetMapping("/mnt")
	public ResObj mnt() {
		return new ResObj();
	}

	private void doWork() {
		ExponentialDistribution dist = new ExponentialDistribution(this.stime);
		Double isTime = dist.getMean();
		Float d = (float) (isTime.floatValue() * (MSController.users.floatValue() / this.hw));
		MSController.users.incrementAndGet();
		try {
			TimeUnit.MILLISECONDS.sleep(Math.max(Math.round(d), Math.round(isTime)));
		} catch (InterruptedException e) {
			e.printStackTrace();
		} finally {
			MSController.users.decrementAndGet();
		}
	}
}
