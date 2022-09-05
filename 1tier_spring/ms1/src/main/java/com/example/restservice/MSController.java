package com.example.restservice;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import org.apache.commons.math3.distribution.ExponentialDistribution;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MSController {
	private static final AtomicInteger users = new AtomicInteger(0);

	@Value("${ms.hw}")
	private Float hw;

	@Value("${ms.name}")
	private static String name;

	@Autowired
	private MongoTemplate mt;

	private final Long stime = 20l;

	@RequestMapping(value = "/", method = RequestMethod.GET)
	@ResponseBody
	public ResObj msGet(@RequestParam(name = "login") String login,@RequestParam(name = "name") String name) {
		System.out.println("Received GET request");
		System.out.println("%s=%s".formatted(new String[] {"login",login}));
		System.out.println("%s=%s".formatted(new String[] {"name",name}));
		this.doWork();
		return new ResObj();
	}

	@RequestMapping(value = "/", method = RequestMethod.POST)
	@ResponseBody
	public ResObj msPost(@RequestParam(name = "login") String login,@RequestParam(name = "name") String name) {
		System.out.println("Received POST request");
		System.out.println("%s=%s".formatted(new String[] {"login",login}));
		System.out.println("%s=%s".formatted(new String[] {"name",name}));
		this.doWork();
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
		} finally {
			MSController.users.decrementAndGet();
		}
	}

	private void doWork() {
		this.doWork(this.stime);
	}

}
