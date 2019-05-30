import requests
import urllib.parse
import threading

# 使用多线程
# 设置最大线程锁
thread_lock = threading.BoundedSemaphore(value=10)
# https://www.duitang.com/napi/blog/list/by_search/?kw=%E7%BE%8E%E5%A5%B3&start=48&limit=1000
# 自己将参数增加到100
# "path": "https://b-ssl.duitang.com/uploads/item/201901/25/20190125203503_orwox.jpeg"
'通过url获取内容'


def get_content(url):
    # requests 自带了json.loads
    response = requests.get(url)
    # decode将bytes转化为字符串
    content = response.content.decode('utf-8')
    return content


# print(get_content('https://www.duitang.com/napi/blog/list/by_search/?kw=%E7%BE%8E%E5%A5%B3&start=48&limit=1000'))
def find_img_url(content, startpart, endpart):
    img_url = []
    end = 0
    # 从end开始找startpart          # find函数找的到返回  ！=-1， 找不到等于-1
    while content.find(startpart, end) != -1:
        start = content.find(startpart, end) + len(startpart)  # 开始的下标
        end = content.find(endpart, start)  # 结束的下标
        src = content[start:end]
        img_url.append(src)
    return img_url


# https://b-ssl.duitang.com/uploads/item/201905/20/20190520124959_gfgwu.thumb.400_0.jpg
def page_from_duitang(label):
    pages = []
    url = 'https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}&limit=1000'
    label = urllib.parse.quote(label)  # 将中文转成ASCII码
    for index in range(0, 3200, 100):
        url = url.format(label, index)
        print(url)
        content = get_content(url)
        pages.append(content)
        return pages


def pic_url_from_pages(pages):
    pic_urls = []
    for page in pages:
        urls = find_img_url(page, 'path":"', '"')
        # extend  将一个列表里面所有的元素加到另一个列表的后面
        pic_urls.extend(urls)
        return pic_urls


def download_pics(url, m):
    r = requests.get(url)
    path = 'pics/' + str(m) + '.jpg'
    with open(path, 'wb') as fp:
        fp.write(r.content)
    # 下载完了  解锁
    thread_lock.release()


if __name__ == '__main__':
    label = '美女'
    m = 0
    pages = page_from_duitang(label)
    pic_urls = pic_url_from_pages(pages)
    for url in pic_urls:
        m += 1
        print('正在下载第{}张图片'.format(m))
        # 线程上锁
        thread_lock.acquire()
        t = threading.Thread(target=download_pics, args=(url, m))
        t.start()
