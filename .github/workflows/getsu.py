# 获取BPB订阅

import concurrent.futures
import threading
import requests
from pathlib import Path
lock = threading.Lock()



# used_sub_lst: list[str] = []


def file_exists(file_path: str):
    """判断文件或者目录是否存在

    Args:
        file_path (str): 文件或者目录的路径

    Returns:
        bool: 返回布尔值
    """
    return Path(f"{file_path}").exists()

def readFile(file_path: str):
    """读取文件所有内容并存到一个字符串中返回

    Args:
        file_path (str): 文件路径

    Returns:
        str: 返回文件内容
    """
    if not file_exists(file_path=file_path):
        return ''
    with open(f"{file_path}",'r',encoding="utf-8") as f:
        text = f.read().strip()
    return text

success_sub_set: set[str] = set(readFile("./success.txt").split("\n",maxsplit=-1))

def makeR(url: str):
    url_full: str = f"https://{url}/sub/89b3cbba-e6ac-485a-9481-976a0415eab9"
    if url_full in success_sub_set:
        print(f"{url_full}已写入,跳过本次请求")
        return
    try:
        res = requests.get(url=url_full,allow_redirects=True,verify=False,timeout=5)
        if res.status_code == 200:
            print(f"{url_full}泄漏,请求成功")
            with lock:
                # used_sub_lst.append(url_full)
                with open("./success.txt",'a',encoding="utf-8") as f:
                    f.write(f"{url_full}\n")
    except Exception as e:
        print(f"{url_full}没有泄漏,请求失败")



all_urls_lst: list[str] = readFile("./domains.csv").split("\n",maxsplit=-1)



threads_nums: int = 4

# new_url_lst: list[list[str]] = pt.listSegment(lst=all_urls_lst,offset_nums=threads_nums)


with concurrent.futures.ThreadPoolExecutor(max_workers=threads_nums) as executor:
    future_list = []
    for e in all_urls_lst:
        for u in e:
            future = executor.submit(makeR,u)
            future_list.append(future)
    concurrent.futures.wait(future_list)
    
url_lst: list[str] = list(set(readFile("./success.txt").split("\n",maxsplit=-1)))
with open("./success.txt",'w',encoding="utf-8") as f2:
    for sub in url_lst:
        # code
        if sub not in {'',' ',"\n"}:
            f2.write(f"{sub}\n")
