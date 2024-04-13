# 漏洞扫描程序

这是一个漏洞扫描程序，用于检测给定的 URL 是否存在特定漏洞。

# 使用指南

## Github

https://github.com/hypnoticp/Python_script

## 准备环境

Python 3

## 命令参数

```
python3 main.py -h
usage: main.py [-h] [-f FILE] [-u URL] [-p POC] [-t THREAD] [-type TYPE]
optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  url文件路径
  -u URL, --url URL     主机地址
  -p POC, --poc POC     poc名,多个以逗号隔开,支持*号模糊匹配
  -t THREAD, --thread THREAD
                        线程数量(默认1500,数量越低，准确率越高)
  -type TYPE            指定漏洞类型目录
-u 或 -f 为必填参数，用于指定单个 URL 或 URL 文件路径进行扫描。
```

-p 为可选参数，用于指定特定的 POC 进行扫描，支持单个、多个、模糊匹配 POC 名称。

-t 为可选参数，用于指定线程数量，默认为 1500，数量越低，扫描准确率越高。

-type 为可选参数，用于指定特定的漏洞类型目录。

## 结果输出

终端输出会打印存在漏洞或不存在漏洞的 URL，以及对应的 POC 名称。

程序运行时，会将存在漏洞的 URL 和 POC 名称保存至当前目录的 vuln.txt 文件中。

## 自定义 POC 编写

您可以在 pocs 目录下编写自定义的 POC 模块。只需在文件中编写一个名为 scan 的函数，该函数接收一个 URL 参数，并根据漏洞情况返回 True 或 False 即可。

## 线程调度

程序使用线程池进行扫描，线程数量可通过 -t 参数进行调整，根据系统资源和扫描准确率进行选择。

# 示例

## 扫描单个 URL：

```
python3 main.py -u http://example.com -p poc-name
```

## 扫描 URL 文件：

```
python3 main.py -f urls.txt -p poc-name -t 1000
```

## 扫描特定漏洞类型目录下的 URL 文件：

```
 python3 main.py -f urls.txt -p poc-name -t 1000 -type vuln-type
```

# 注意事项

程序仅供学习和研究使用，请勿用于非法目的。

对于自定义 POC 的编写，请确保代码质量和安全性，避免因为漏洞验证不准确导致误判或误报。

# 作者

本程序由 hypnotic编写，如有任何问题或建议，请联系 w2598829114@163.com
