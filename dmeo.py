import os

def count_files_in_drive(drive_letter):
    try:
        # 构建指定驱动器的绝对路径
        drive_path = f"{drive_letter}:\\"

        # 获取指定驱动器下的所有文件和文件夹
        files = []
        for root, dirs, filenames in os.walk(drive_path):
            files.extend(filenames)

        # 统计文件的数量
        file_count = len(files)

        return file_count

    except Exception as e:
        print(f"发生错误: {e}")
        return None

# 统计C盘下的文件数量
c_drive_count = count_files_in_drive("C")

# 统计D盘下的文件数量
d_drive_count = count_files_in_drive("D")

# 打印结果
if c_drive_count is not None:
    print(f"C盘下的文件数量为: {c_drive_count}")
else:
    print("无法统计C盘下的文件数量")

if d_drive_count is not None:
    print(f"D盘下的文件数量为: {d_drive_count}")
else:
    print("无法统计D盘下的文件数量")
