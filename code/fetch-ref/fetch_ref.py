import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

def normalize_url(href):
    """确保链接前缀不重复"""
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return "https://dblp.org" + href

def extract_title(entry):
    """
    从一整行文献条目中提取标题
    格式示例：
      "2. Zu-Ming Jiang ... Dynsql: Stateful fuzzing ... In USENIX ..."
    规则：
      作者之后第一个句号后的内容直到 "In <Venue>"
    """
    # 去掉前面的 "2. "
    entry = entry.strip()
    entry = re.sub(r"^\d+\.\s*", "", entry)

    # 用正则捕获 "标题. In Venue"
    # 非贪婪提取标题部分
    m = re.search(r"\.\s*(.*?)\.\s*In\s", entry)
    
    if m:
        return m.group(1).strip()

    print("⚠️ 未能解析标题，使用全文作为搜索：", entry)
    return entry


def fetch_bibtex_from_dblp(title):
    print(f"\n=== 查找：{title} ===")
    query = urllib.parse.quote(title)
    search_url = f"https://dblp.org/search?q={query}"

    # Step 1: 搜索页面
    resp = requests.get(search_url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Step 2: 找到第一个含 view=bibtex 的链接
    bib_link = None
    for a in soup.find_all("a", href=True):
        if "view=bibtex" in a["href"]:
            bib_link = normalize_url(a["href"])
            break

    if not bib_link:
        print("❌ 未找到 BibTeX 链接")
        return None

    print(f"找到 BibTeX 链接：{bib_link}")

    # Step 3: 获取 BibTeX 页面
    resp2 = requests.get(bib_link, headers=HEADERS, timeout=15)
    soup2 = BeautifulSoup(resp2.text, "html.parser")

    # Step 4: 提取 BibTeX
    pre = soup2.find("pre", class_="verbatim")
    if pre is None:
        print("❌ 未找到 BibTeX 内容")
        return None

    return pre.text.strip()


if __name__ == "__main__":
    raw = """1. Yongle Zhang, Kirk Rodrigues, Yu Luo, Michael Stumm, and Ding Yuan. The inflection point hypothesis: a principled debugging approach for locating the root cause of a failure. In SOSP, pages 131–146, 2019.
2. Xiang Jenny Ren, Sitao Wang, Zhuqi Jin, David Lion, Adrian Chiu, Tianyin Xu, and Ding Yuan. Relational debugging—pinpointing root causes of performance problems. In OSDI, pages 65–80, 2023.
3. Dewei Liu, Chuan He, Xin Peng, Fan Lin, Chenxi Zhang, Shengfang Gong, Ziang Li, Jiayu Ou, and Zheshun Wu. Microhecl: High-efficient root causes localization in large-scale microservice systems. In ICSE, pages 338–347, 2021.
4. Xu Wang, Hongwei Yu, Xiangxin Meng, Hongliang Cao, Hongyu Zhang, Hailong Sun, Xudong Liu, and Chunming Hu. Mtl-transfer: Leveraging multi-task learning and transferred knowledge for improving fault localization and program repair. In ACM Transactions on Software Engineering and Methodology, 2024.
5. Aidan ZH Yang, Claire Le Goues, Ruben Martins, and Vincent Hellendoorn. Large language models for test-free fault localization. In ICSE, pages 1–12, 2024.
6.  Xuanhe Zhou, Guoliang Li, Zhaoyan Sun, Zhiyuan Liu, Weize Chen, Jianming Wu, Jiesi Liu, Ruohang Feng, and Guoyang Zeng. D-bot: Database diagnosis system using large language models. In arXiv preprint arXiv:2312.01454, 2023."""

    raw_entries = raw.strip().split("\n")

    # 自动提取标题
    titles = [extract_title(e) for e in raw_entries]
    with open("dblp_bibtex_results.bib", "w") as f:
        # 抓取 bibtex
        for t in titles:
            bib = fetch_bibtex_from_dblp(t)
            if bib:
                print("\n------ BibTeX ------")
                print(bib)
                print(bib,file=f)
                print("--------------------")
            time.sleep(1)
