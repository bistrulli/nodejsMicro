package com.example.restservice;

import java.util.ArrayList;

import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document
public class Ms {
	@Id
	ObjectId databaseId;
	private int id;

	private String type;
	private String appFile;
	private String addr;
	private Integer replica;
	private String prxFile;
	private Float hw;
	private ArrayList<Integer> ports;
	private Integer prxPort;
	private String name;

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

	public String getAppFile() {
		return appFile;
	}

	public void setAppFile(String appFile) {
		this.appFile = appFile;
	}

	public String getAddr() {
		return addr;
	}

	public void setAddr(String addr) {
		this.addr = addr;
	}

	public Integer getReplica() {
		return replica;
	}

	public void setReplica(Integer replica) {
		this.replica = replica;
	}

	public String getPrxFile() {
		return prxFile;
	}

	public void setPrxFile(String prxFile) {
		this.prxFile = prxFile;
	}

	public Float getHw() {
		return hw;
	}

	public void setHw(Float hw) {
		this.hw = hw;
	}

	public ArrayList<Integer> getPorts() {
		return ports;
	}

	public void setPorts(ArrayList<Integer> ports) {
		this.ports = ports;
	}

	public Integer getPrxPort() {
		return prxPort;
	}

	public void setPrxPort(Integer prxPort) {
		this.prxPort = prxPort;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

}