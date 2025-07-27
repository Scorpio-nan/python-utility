import os
import zipfile
import rarfile
from tqdm import tqdm  # 进度条支持，可选安装


def find_compressed_files(root_dir, extensions=('.zip', '.rar')):
    """
    递归查找指定目录下的压缩文件
    :param root_dir: 要搜索的根目录
    :param extensions: 要查找的文件扩展名
    :return: 找到的压缩文件路径列表
    """
    compressed_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(extensions):
                compressed_files.append(os.path.join(dirpath, filename))
    return compressed_files


def extract_zip(zip_path, extract_to=None, delete_after=False):
    """
    解压ZIP文件
    :param zip_path: ZIP文件路径
    :param extract_to: 解压目录(默认为ZIP文件所在目录)
    :param delete_after: 解压后是否删除原文件
    """
    if extract_to is None:
        extract_to = os.path.dirname(zip_path)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"成功解压: {zip_path} -> {extract_to}")

        if delete_after:
            os.remove(zip_path)
            print(f"已删除原文件: {zip_path}")
    except Exception as e:
        print(f"解压ZIP失败 {zip_path}: {str(e)}")


def extract_rar(rar_path, extract_to=None, delete_after=False):
    """
    解压RAR文件
    :param rar_path: RAR文件路径
    :param extract_to: 解压目录(默认为RAR文件所在目录)
    :param delete_after: 解压后是否删除原文件
    """
    if extract_to is None:
        extract_to = os.path.dirname(rar_path)

    try:
        with rarfile.RarFile(rar_path, 'r') as rar_ref:
            rar_ref.extractall(extract_to)
        print(f"成功解压: {rar_path} -> {extract_to}")

        if delete_after:
            os.remove(rar_path)
            print(f"已删除原文件: {rar_path}")
    except Exception as e:
        print(f"解压RAR失败 {rar_path}: {str(e)}")


def batch_extract(root_dir, delete_after=False):
    """
    批量解压目录下的所有压缩文件
    :param root_dir: 根目录路径
    :param delete_after: 解压后是否删除原文件
    """
    # 查找所有压缩文件
    compressed_files = find_compressed_files(root_dir)

    if not compressed_files:
        print(f"在 {root_dir} 中未找到任何ZIP或RAR文件")
        return

    print(f"共找到 {len(compressed_files)} 个压缩文件")

    # 使用进度条(需要安装tqdm库)
    for file_path in tqdm(compressed_files, desc="解压进度"):
        if file_path.lower().endswith('.zip'):
            extract_zip(file_path, delete_after=delete_after)
        elif file_path.lower().endswith('.rar'):
            extract_rar(file_path, delete_after=delete_after)


if __name__ == "__main__":
    import argparse

    # 设置命令行参数
    parser = argparse.ArgumentParser(description="递归解压目录下的ZIP和RAR文件")
    parser.add_argument("directory", help="要搜索的目录路径")
    parser.add_argument("--delete", action="store_true", help="解压后删除原压缩文件")
    args = parser.parse_args()

    # 检查目录是否存在
    if not os.path.isdir(args.directory):
        print(f"错误: 目录 {args.directory} 不存在")
        exit(1)

    # 检查rarfile是否安装
    try:
        import rarfile
    except ImportError:
        print("警告: 未安装rarfile库，将无法解压RAR文件")
        print("请安装: pip install rarfile")
        # 继续运行，只是不能解压RAR

    # 执行解压
    batch_extract(args.directory, delete_after=args.delete)

# python unzip-files.py D:\workspace\资源\PPT模板