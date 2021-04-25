package com.test.util;

import java.util.concurrent.ConcurrentHashMap;

import com.alibaba.fastjson.JSONObject;

public class JsonUtil {

	private static ConcurrentHashMap<String, JSONObject> concurrentHashMap = new ConcurrentHashMap<String, JSONObject>();

	public static void put(int index) {
		JSONObject jsonObject = getJSONObject();
		switch (index) {
		case -1:
			jsonObject.put("code", -1);
			jsonObject.put("msg", "业务未执行成功");
			break;
		case 200:
			jsonObject.put("code", 200);
			jsonObject.put("msg", "成功");
			break;
		case 301:
			jsonObject.put("code", 301);
			jsonObject.put("msg", "重定向到");
			jsonObject.put("data", "/index");
			break;
		case 403:
			jsonObject.put("code", 403);
			jsonObject.put("msg", "拒绝请求");
			break;
		case 405:
			jsonObject.put("code", 405);
			jsonObject.put("msg", "不满足操作条件");
			jsonObject.put("data", "/index");
			break;
		case 500:
			jsonObject.put("code", 500);
			jsonObject.put("msg", "服务器执行失败");
			break;

		}
	}

	public static void put(int index, Object objct, String msg) {
		JSONObject jsonObject = getJSONObject();
		jsonObject.put("code", index);
		jsonObject.put("data", objct);
		jsonObject.put("msg", msg);
	}

	public static void put(int index, Object objct) {
		JSONObject jsonObject = getJSONObject();
		jsonObject.put("code", index);
		jsonObject.put("data", objct);
	}

	public static void put(Object objct) {
		JSONObject jsonObject = getJSONObject();
		jsonObject.put("code", 200);
		jsonObject.put("data", objct);
	}

	public static void put(String key, Object data) {
		JSONObject jsonObject = getJSONObject();
		jsonObject.put(key, data);
	}

	public static String toJSONString() {
		JSONObject jsonObject = getJSONObject();
		String resData = jsonObject.toJSONString();
		jsonObject.clear();
		return resData;
	}

	public static void put(boolean b) {
		put(b ? 200 : -1);
	}

	public static JSONObject getJSONObject() {

		String threadName = Thread.currentThread().getName();
		if (concurrentHashMap.containsKey(threadName)) {
			return concurrentHashMap.get(threadName);
		} else {
			JSON.DEFAULT_GENERATE_FEATURE |= SerializerFeature.DisableCircularReferenceDetect.getMask();
			JSONObject jsonObject = new JSONObject();
			concurrentHashMap.put(threadName, jsonObject);
			return jsonObject;
		}

	}
}

