
"""  图片压缩脚本  """

import os
from PIL import Image
from pathlib import Path
import sys
import time

SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')


class ImageCompressor:
    def __init__(self, input_dir, output_dir, quality=85, optimize=True):
        self.input_dir = Path(input_dir).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.quality = quality
        self.optimize = optimize
        self.stats = {
            'processed': 0,
            'skipped': 0,
            'original_size': 0,
            'compressed_size': 0,
            'errors': []
        }
        self.start_time = time.time()

        # 创建输出根目录
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _should_process(self, file_path):
        """判断是否为需要处理的图片文件"""
        return file_path.suffix.lower() in SUPPORTED_EXTENSIONS

    def _get_output_path(self, input_path):
        """生成保留目录结构的输出路径"""
        # 获取相对输入目录的路径
        relative_path = input_path.relative_to(self.input_dir)
        # 生成输出路径
        return self.output_dir / relative_path

    def _process_image(self, input_path):
        """处理单个图片文件"""
        try:
            output_path = self._get_output_path(input_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with Image.open(input_path) as img:
                """
                # 保留原始模式（如RGBA、LA等）
                if img.mode in ('RGBA', 'LA'):
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')
                """
                # 增强模式转换逻辑
                if img.mode == 'P' and 'transparency' in img.info:
                    img = img.convert('RGBA')
                elif img.mode in ('RGBA', 'LA'):
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')

                save_args = {
                    'quality': self.quality,
                    'optimize': self.optimize
                }

                # 根据文件类型调整保存参数
                if input_path.suffix.lower() in ('.png', '.bmp'):
                    img.save(output_path, **save_args, compress_level=9)
                else:
                    img.save(output_path, **save_args)

                original_size = input_path.stat().st_size
                compressed_size = output_path.stat().st_size
                return (original_size, compressed_size)

        except Exception as e:
            self.stats['errors'].append(f"{input_path}: {str(e)}")
            return None

    def _print_progress(self, current, total):
        """打印处理进度"""
        progress = current / total
        bar_length = 40
        filled = int(bar_length * progress)
        bar = '#' * filled + '-' * (bar_length - filled)
        sys.stdout.write(f"\rProcessing: [{bar}] {progress:.1%}")
        sys.stdout.flush()

    def run(self):
        """执行压缩操作"""
        # 获取所有需要处理的文件
        all_files = []
        for root, _, files in os.walk(self.input_dir):
            for file in files:
                path = Path(root) / file
                if self._should_process(path):
                    all_files.append(path)

        total_files = len(all_files)
        print(f"Found {total_files} image files to process")
        print(f"输出目录: {self.output_dir}")

        for i, file_path in enumerate(all_files, 1):
            self._print_progress(i, total_files)

            try:
                # 记录原始文件大小
                original_size = file_path.stat().st_size
                result = self._process_image(file_path)

                if result:
                    self.stats['processed'] += 1
                    self.stats['original_size'] += result[0]
                    self.stats['compressed_size'] += result[1]
                else:
                    self.stats['skipped'] += 1
            except Exception as e:
                self.stats['errors'].append(f"{file_path}: {str(e)}")
                self.stats['skipped'] += 1

        # 打印最终统计
        print("\n\nCompression complete!")
        print(f"已处理文件数量: {self.stats['processed']}")
        print(f"跳过文件数量: {self.stats['skipped']}")
        print(f"原始文件总大小: {self.stats['original_size'] / 1024 / 1024:.2f} MB")
        print(f"压缩后文件总大小: {self.stats['compressed_size'] / 1024 / 1024:.2f} MB")
        print(f"节省空间: {(self.stats['original_size'] - self.stats['compressed_size']) / 1024 / 1024:.2f} MB")
        print(f"处理时长: {time.time() - self.start_time:.2f} seconds")

        if self.stats['errors']:
            print("\n发生错误:")
            for error in self.stats['errors']:
                print(f"  - {error}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python compress_images.py <input_directory> <output_directory>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist")
        sys.exit(1)

    # 配置压缩参数（可自定义调整）
    compressor = ImageCompressor(
        input_dir=input_dir,
        output_dir=output_dir,
        quality=80,  # 推荐质量参数：80-85
        optimize=True  # 启用优化选项
    )

    compressor.run()

#  pip install pillow
#  eg: python .\image-compress.py E:\images E:\compressed_images
