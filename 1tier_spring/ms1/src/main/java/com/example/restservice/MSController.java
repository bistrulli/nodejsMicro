package com.example.restservice;

import java.util.concurrent.atomic.AtomicInteger;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import ctrlmnt.ControllableService;

@RestController
public class MSController extends ControllableService {

	@Value("${ms.hw}")
	private Float hw;

	@Value("${ms.name}")
	private String msname;
	
	private static final AtomicInteger users = new AtomicInteger(0);

	@Autowired
	private MongoTemplate mt;

	private final Long stime = 100l;

	@RequestMapping(value = "/", method = RequestMethod.GET)
	@ResponseBody
	public ResObj msGet(@RequestParam(name = "login") String login,@RequestParam(name = "name") String name) {
//		System.out.println("Received GET request");
//		System.out.println("%s=%s".formatted(new String[] {"login",login}));
//		System.out.println("%s=%s".formatted(new String[] {"name",name}));
		System.out.println(this.getHw());
		this.doWork(this.stime);
		return new ResObj();
	}

	@RequestMapping(value = "/", method = RequestMethod.POST)
	@ResponseBody
	public ResObj msPost(@RequestParam(name = "login") String login,@RequestParam(name = "name") String name) {
//		System.out.println("Received POST request");
//		System.out.println("%s=%s".formatted(new String[] {"login",login}));
//		System.out.println("%s=%s".formatted(new String[] {"name",name}));
		this.doWork(this.stime);
		return new ResObj();
	}

	@GetMapping("/mnt")
	public ResObj mnt() {
		return new ResObj();
	}

	@Override
	public Float getHw() {
		return this.hw;
	}

	@Override
	public String getName() {
		return this.msname;
	}

	@Override
	public void setHw(Float hw) {
		this.hw = hw;
	}

	@Override
	public void egress() {
		MSController.users.decrementAndGet();
	}

	@Override
	public Integer getUser() {
		return MSController.users.get();
	}

	@Override
	public void ingress() {
		MSController.users.incrementAndGet();
	}

}
