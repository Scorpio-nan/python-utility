import os
import zipfile
import argparse
from pathlib import Path
import logging
from typing import List

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ZipExtractor:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.supported_extensions = ['.zip']

    def find_zip_files(self) -> List[Path]:
        """查找所有ZIP文件"""
        zip_files = []
        for ext in self.supported_extensions:
            zip_files.extend(self.base_dir.glob(f"*{ext}"))
        return zip_files

    def extract_zip(self, zip_file: Path, extract_to: Path = None, delete_original: bool = True) -> bool:
        """
        解压单个ZIP文件

        Args:
            zip_file: ZIP文件路径
            extract_to: 解压目标目录（None则使用文件名）
            delete_original: 是否删除原文件

        Returns:
            bool: 是否成功
        """
        try:
            if not zip_file.exists():
                logger.error(f"文件不存在: {zip_file}")
                return False

            # 确定解压目录
            if extract_to is None:
                extract_to = self.base_dir / zip_file.stem

            # 创建解压目录
            extract_to.mkdir(parents=True, exist_ok=True)

            # 解压文件
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # 检查文件数量
                file_count = len(zip_ref.namelist())
                logger.info(f"解压 {zip_file.name} (包含 {file_count} 个文件) -> {extract_to.name}")

                # 解压所有文件
                zip_ref.extractall(extract_to)

            # 删除原文件
            if delete_original:
                zip_file.unlink()
                logger.info(f"已删除原文件: {zip_file.name}")

            return True

        except zipfile.BadZipFile:
            logger.error(f"文件损坏或不是有效的ZIP文件: {zip_file.name}")
            return False
        except PermissionError:
            logger.error(f"权限不足，无法操作文件: {zip_file.name}")
            return False
        except Exception as e:
            logger.error(f"解压失败 {zip_file.name}: {str(e)}")
            return False

    def extract_all_zips(self, delete_original: bool = True, recursive: bool = False) -> dict:
        """
        解压所有ZIP文件

        Args:
            delete_original: 是否删除原文件
            recursive: 是否递归处理子目录

        Returns:
            dict: 处理结果统计
        """
        if recursive:
            zip_files = []
            for root, _, files in os.walk(self.base_dir):
                for file in files:
                    if any(file.endswith(ext) for ext in self.supported_extensions):
                        zip_files.append(Path(root) / file)
        else:
            zip_files = self.find_zip_files()

        if not zip_files:
            logger.info("没有找到ZIP文件")
            return {"total": 0, "success": 0, "failed": 0}

        logger.info(f"找到 {len(zip_files)} 个ZIP文件")

        results = {"total": len(zip_files), "success": 0, "failed": 0}

        for zip_file in zip_files:
            if self.extract_zip(zip_file, delete_original=delete_original):
                results["success"] += 1
            else:
                results["failed"] += 1

        logger.info(f"处理完成: 总共 {results['total']} 个, 成功 {results['success']} 个, 失败 {results['failed']} 个")
        return results


def main():
    parser = argparse.ArgumentParser(description='解压目录下的所有ZIP文件')
    parser.add_argument('directory', nargs='?', default='.', help='要处理的目录路径（默认为当前目录）')
    parser.add_argument('--no-delete', action='store_false', dest='delete_original',
                        help='不解压后删除原ZIP文件')
    parser.add_argument('--recursive', '-r', action='store_true',
                        help='递归处理子目录中的ZIP文件')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='详细输出模式')

    args = parser.parse_args()

    # 设置日志级别
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # 检查目录是否存在
    target_dir = Path(args.directory)
    if not target_dir.exists():
        logger.error(f"目录不存在: {target_dir}")
        return 1

    if not target_dir.is_dir():
        logger.error(f"不是目录: {target_dir}")
        return 1

    # 创建解压器实例并执行
    extractor = ZipExtractor(target_dir)
    results = extractor.extract_all_zips(
        delete_original=args.delete_original,
        recursive=args.recursive
    )

    return 0 if results["failed"] == 0 else 1


if __name__ == "__main__":
    exit(main())