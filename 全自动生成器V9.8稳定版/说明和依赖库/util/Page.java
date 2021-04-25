package com.test.util;

import com.alibaba.fastjson.JSON;

public class Page {
	private int start = 0;
	private int count = 10;
	private int max;
	private int page = 1;
	private int maxPage;

	public int getStart() {
		return start;
	}

	public void setStart(int start) {
		this.start = start;
	}

	public int getCount() {
		return count;
	}

	public void setCount(int count) {
		this.count = count;
	}

	public int getMax() {
		return max;
	}

	public void setMax(int max) {
		this.max = max;
		int tempPage = max / count;
		int tempFlag = max % count == 0 ? 0 : 1;
		this.maxPage = tempPage + tempFlag;
	}

	public int getPage() {
		return page;
	}

	public void setPage(int page) {
		this.page = page > 0 ? page : 1;
		this.start = this.count * (this.page - 1);
	}

	public int getMaxPage() {
		return maxPage;
	}

	public void setMaxPage(int maxPage) {
		this.maxPage = maxPage;
	}

	@Override
	public String toString() {
		return JSON.toJSONString(this);
	}

}
