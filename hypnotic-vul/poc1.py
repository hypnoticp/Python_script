import argparse
import os
import sys
import importlib.util
import concurrent.futures

# 定义一个用于导入POC模块的函数
def import_pocs(poc_dir, poc_type=None):
    poc_modules = {}
    if poc_type:
        poc_type_dir = os.path.join(poc_dir, poc_type)
        if not os.path.exists(poc_type_dir):
            print(f"错误：指定的漏洞类型目录 {poc_type} 不存在")
            sys.exit(1)
        poc_files = [f for f in os.listdir(poc_type_dir) if f.endswith(".py")]
        for file in poc_files:
            poc_name = file[:-3]
            spec = importlib.util.spec_from_file_location(poc_name, os.path.join(poc_type_dir, file))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            poc_modules[poc_name] = module
    else:
        for root, dirs, files in os.walk(poc_dir):
            for file in files:
                if file.endswith(".py"):
                    poc_name = file[:-3]
                    spec = importlib.util.spec_from_file_location(poc_name, os.path.join(root, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    poc_modules[poc_name] = module
    return poc_modules

# 定义一个用于处理URL的函数
def process_urls(file_path):
    if not os.path.exists(file_path):
        print("错误：指定的文件路径不存在")
        sys.exit(1)
    with open(file_path, "r") as f:
        urls = f.read().strip().split("\n")
    return urls

# 定义一个用于扫描漏洞的函数
def scan_vulnerabilities(url, poc_name, poc_modules):
    try:
        if poc_name in poc_modules:
            if poc_modules[poc_name].scan(url):
                print(f"[+] {url} 存在漏洞 {poc_name}")
                with open("vuln.txt", "a") as f:
                    f.write(f"{url} {poc_name}\n")
            else:
                print(f"[-] {url} 不存在漏洞 {poc_name}")
        else:
            print(f"[!] POC {poc_name} 不存在")
    except Exception as e:
        print(f"[!] 发生异常：{e}，无法验证 {url} {poc_name}")

# 定义主函数
def main():
    parser = argparse.ArgumentParser(description="漏洞扫描程序")
    parser.add_argument("-f", "--file", help="url文件路径")
    parser.add_argument("-u", "--url", help="主机地址")
    parser.add_argument("-p", "--poc", help="poc名,多个以逗号隔开,支持*号模糊匹配")
    parser.add_argument("-t", "--thread", type=int, default=1500, help="线程数量(默认1500,数量越低，准确率越高)")
    parser.add_argument("-type", help="指定漏洞类型目录")
    args = parser.parse_args()

    if not (args.file or args.url):
        print("错误：-u 或 -f 参数为必填")
        parser.print_help()
        sys.exit(1)

    poc_dir = "pocs"
    poc_type = args.type
    poc_modules = import_pocs(poc_dir, poc_type)

    urls = process_urls(args.file) if args.file else [args.url]
    poc_names = args.poc.split(",") if args.poc else poc_modules.keys()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.thread) as executor:
        for url in urls:
            for poc_name in poc_names:
                executor.submit(scan_vulnerabilities, url, poc_name, poc_modules)

if __name__ == "__main__":
    main()

