package com.galgame.util;

import java.util.ArrayList;
import java.util.Date;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.servlet.http.HttpServletRequest;

import java.math.BigInteger;
import java.security.*;
import java.text.SimpleDateFormat;

public class StringUtil {

	private static Random random = new Random();
	private static SimpleDateFormat simpleDateFormatDatetime = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
	private static SimpleDateFormat simpleDateFormatDate = new SimpleDateFormat("yyyy-MM-dd");

	public static boolean eq(String el, String str) {
		if (str == null) {
			return false;
		}
		Pattern pattern = Pattern.compile(el);
		Matcher matcher = pattern.matcher(str);
		return matcher.matches();
	}

	public static boolean eqUserName(String str) {
		if (str != null) {
			String el = "^\\w{4,16}$";
			return eq(el, str);
		}
		return false;
	}

	public static boolean eqPassword(String str) {
		if (str != null) {
			String el = "^\\w{4,16}$";
			return eq(el, str);
		}
		return false;
	}

	public static boolean eqEmail(String str) {
		if (str != null) {
			String el = "^\\w+@\\w+\\.\\w+$";
			return eq(el, str);
		}
		return false;
	}

	public static boolean eqPhone(String str) {
		if (str != null) {
			String el = "^1[3458]\\d{9}$";
			return eq(el, str);
		}
		return false;
	}

	public static Integer parseInt(String str) {
		try {
			return Integer.parseInt(str);
		} catch (Exception e) {
			return 0;
		}

	}

	public static boolean isNotAllSpaceOrNULL(String str) {
		if (str == null || str.length() == 0) {
			return false;
		}
		for (int i = 0; i < str.length(); i++) {
			if (str.charAt(i) != ' ') {
				return true;
			}
		}
		return false;
	}

	public static String randomStringByUUID() {
		return UUID.randomUUID().toString().replace("-", "");

	}

	public static String randomStringByUUID(int length) {
		String data = UUID.randomUUID().toString().replace("-", "");
		length = length < 1 ? data.length() : length;
		if (data.length() > length) {
			data = data.substring(0, length);
		}
		return data;

	}

	public static String randomString() {
		return randomString(8);
	}

	public static String randomString(int length) {
		return randomString(null, length);
	}

	public static String randomStringCode() {
		return randomStringCode(6);
	}

	public static String randomStringCode(int length) {
		String data = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789";
		return randomString(data, length);
	}

	public static String randomString(String data, int length) {
		length = length < 1 ? 4 : length;
		if (data == null || data.length() == 0) {
			data = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz0123456789";
		}
		String code = "";
		for (int i = 0; i < length; i++) {
			code += data.charAt(random.nextInt(data.length()));
		}
		return code;
	}

	public static String getFileFormat(String fileName) {
		int i = fileName.lastIndexOf(".");
		if (i != -1) {
			return fileName.substring(i, fileName.length());
		} else {
			return "";
		}
	}

	public static String chikeFileNameIsImg(String fileName) {
		String s = getFileFormat(fileName);
		if (s.equalsIgnoreCase(".jpg")) {
			return ".jpg";
		}
		if (s.equalsIgnoreCase(".png")) {
			return ".png";
		}
		if (s.equalsIgnoreCase(".gif")) {
			return ".gif";
		}
		return null;
	}

	public static boolean returnIntegerChike(Integer i) {
		if (i == null || i < 1) {
			return false;
		} else {
			return true;
		}
	}

	public static String getSHA265(String input) {

		try {
			MessageDigest md = MessageDigest.getInstance("SHA-256");
			byte[] messageDigest = md.digest(input.getBytes());

			BigInteger no = new BigInteger(1, messageDigest);
			String hashtext = no.toString(16);
			while (hashtext.length() < 32) {
				hashtext = "0" + hashtext;
			}
			return hashtext;
		}

		catch (NoSuchAlgorithmException e) {
			System.out.println("Exception thrown" + " for incorrect algorithm: " + e);
			return input;
		}
	}

	public static List<Integer> randIntLinkedList(int n, int max) {
		if (n > max) {
			return null;
		}
		List<Integer> list1 = new LinkedList<Integer>();
		int i = 0;
		for (i = 0; i < max; i++) {
			list1.add(i + 1);
		}
		List<Integer> list = new LinkedList<Integer>();
		Random rand = new Random();
		int index = 0;
		for (i = 0; i < n; i++) {
			index = rand.nextInt(list1.size());
			list.add(list1.get(index));
			list1.remove(index);
		}

		return list;

	}

	public static List<Integer> randIntArrayList(int n, int max) {
		if (n > max) {
			return null;
		}
		List<Integer> list1 = new LinkedList<Integer>();
		int i = 0;
		for (i = 0; i < max; i++) {
			list1.add(i + 1);
		}
		List<Integer> list = new ArrayList<Integer>();
		Random rand = new Random();
		int index = 0;
		for (i = 0; i < n; i++) {
			index = rand.nextInt(list1.size());
			list.add(list1.get(index));
			list1.remove(index);
		}
		return list;

	}

	public static String replaceStringSpace(String str) {
		if (str != null) {
			str = str.replace("　", "");
			str = str.replace(" ", "");
			str = str.length() > 0 ? str : null;
		}
		return str;
	}

	public static String trim(String str) {
		if (str != null) {
			str = str.trim();
			str = str.length() > 0 ? str : null;
		}
		return str;
	}

	public static int randInt(int max) {
		return random.nextInt(max);
	}

	public static int randInt(int min, int max) {
		int a;
		if (min > max) {
			a = min;
			min = max;
			max = a;
		}
		a = max - min;
		return random.nextInt(a) + min;
	}

	public static String getRequestIP(HttpServletRequest request) {
		if (request == null) {
			return null;
		}
		String ip = request.getHeader("x-forwarded-for");
		if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
			ip = request.getHeader("Proxy-Client-IP");
		}
		if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
			ip = request.getHeader("WL-Proxy-Client-IP");
		}
		if (ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)) {
			ip = request.getRemoteAddr();
		}
		return ip;

	}

	public static String mailHide(String str) {
		return mailHide(str, 3);
	}

	public static String mailHide(String str, int index) {
		index = index < 1 ? 3 : index;
		if (eqEmail(str)) {
			int end = str.indexOf("@");
			String less = str.substring(end);
			String head = str.substring(0, end);
			if (index > head.length()) {
				index = head.length() - 1;
			}
			int l = head.length() - index;
			head = head.substring(0, index);
			for (int i = 0; i < l; i++) {
				head += "*";
			}
			str = head + less;
		}
		return str;
	}

	public static String phoneHide(String str) {
		if (eqPhone(str)) {
			str = str.substring(0, 3) + "*****" + str.substring(8, 11);
		}
		return str;
	}

	public static boolean eqString(String str1, String str2) {
		return str1 != null ? str1.equals(str2) : false;
	}

	public static boolean eqIgnoreCase(String str1, String str2) {
		return str1 != null ? str1.equalsIgnoreCase(str2) : false;
	}

	public static boolean eqIgnoreCase(Object obj1, Object obj2) {
		return eqIgnoreCase(obj1 == null ? null : obj1.toString(), obj2 == null ? null : obj2.toString());
	}

	public static String getNotDateTime() {
		return simpleDateFormatDatetime.format(new Date());
	}

	public static String getNotDate() {
		return simpleDateFormatDate.format(new Date());
	}

	public static boolean eqInteger(Integer a, Integer b) {
		return a != null ? a.equals(b) : false;
	}

}
