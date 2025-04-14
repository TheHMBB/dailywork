# 获取BPB订阅

import PythonTools as pt

import concurrent.futures
import threading
lock = threading.Lock()



# used_sub_lst: list[str] = []
success_sub_set: set[str] = set(pt.readFile("./泄漏的BPB订阅.txt").split("\n",maxsplit=-1))

def makeR(url: str):
    url_full: str = f"https://{url}/sub/89b3cbba-e6ac-485a-9481-976a0415eab9"
    if url_full in success_sub_set:
        print(f"{url_full}已写入,跳过本次请求")
        return
    try:
        res = pt.requests.get(url=url_full,allow_redirects=True,verify=False,timeout=5)
        if res.status_code == 200:
            print(f"{url_full}泄漏,请求成功")
            with lock:
                # used_sub_lst.append(url_full)
                with open("./泄漏的BPB订阅.txt",'a',encoding="utf-8") as f:
                    f.write(f"{url_full}\n")
    except Exception as e:
        print(f"{url_full}没有泄漏,请求失败")

# all_urls_lst: list[str] = pt.getAllKeysFromDict(pt.jsonFileToDict(json_file_path="./有效的BPB域名排序.json"))
all_urls_lst: list[str] = pt.readFile("./下载的所有BPB域名.csv").split("\n",maxsplit=-1)



threads_nums: int = pt.getMaxThreadsBasedOnResources()

new_url_lst: list[list[str]] = pt.listSegment(lst=all_urls_lst,offset_nums=threads_nums)


with concurrent.futures.ThreadPoolExecutor(max_workers=threads_nums) as executor:
    future_list = []
    for e in new_url_lst:
        for u in e:
            future = executor.submit(makeR,u)
            future_list.append(future)
    concurrent.futures.wait(future_list)
    
url_lst: list[str] = list(set(pt.readFile("./泄漏的BPB订阅.txt").split("\n",maxsplit=-1)))
with open("./泄漏的BPB订阅.txt",'w',encoding="utf-8") as f2:
    for sub in url_lst:
        # code
        if sub not in {'',' ',"\n"}:
            f2.write(f"{sub}\n")
