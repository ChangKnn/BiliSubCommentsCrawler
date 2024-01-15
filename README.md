# B站子评论爬虫

目前（2024/01/15）使用[MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)只能爬取B站主评论，个人需求还需要爬取子评论。因此写了小段程序进行补充，爬取得到子评论内容以及赞数。

在使用MediaCrawler爬取主评论后，利用爬取得到的主评论数据，对各主评论的子评论进行爬取。

## 使用方法

```shell
python main.py -i [input file] -o [output file] -cookie [bili cookie]
```

e.g.

```shell
python main.py -i detail_comments_2024-01-15.csv -cookie "bili cookie"
```

### 参数

```shell
-i
MediaCrawler爬取得到的主评论文件

-o
[可选]输出文件名

-cookie
用户B站cookie
```

## 其他

可通过调整以下参数来设置爬取速度：

```shell
config.PAGE_COMMENTS_NUM
每次请求爬取子评论数（最大20）
```

为防止被ban，在crawl中设置了休眠时间，可自行调整。

```python
sleep_interval = random.random() * 10
time.sleep(sleep_interval)
if sleep_interval > 9.9:    # 1% sleep prevent blocking.
    time.sleep(60)  # Sleep 60s
```
