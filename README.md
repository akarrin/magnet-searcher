# magnet-searcher

磁链聚合搜索命令行工具

![screenshot](https://raw.githubusercontent.com/akarrin/magnet-searcher/master/images/screenshot.gif)


## 安装

```shell
$ git clone https://github.com/akarrin/magnet-searcher.git
$ cd magnet-searcher
$ pip install -r requirements.txt
$ sudo python setup.py install
```

## 使用

```shell
$ magnet-searcher -k 上海堡垒
```

命令选项：

- `-k `、`--keyword`：搜索关键字，必填，可用空格分隔
- `-c`、`--count`：需求的数量，选填
- `-s`、`--sort`：搜索排序，选填，可选size、date、hot
- `--source`：优先搜索的来源，来源可在`rules.json`中自配置
- `--help`：获取命令帮助

## 配置项

- 在`config.ini`文件中配置代理、请求头、请求超时时间、debug模式
- 在`rules.json`中增减搜索来源，或使其中的搜索源失效
- 不配置代理会使`rules.json`中`proxy_channel = true`的规则失效


