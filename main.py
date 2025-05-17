import os
import shutil
import pandas as pd
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def batch_filename(directory, prefix):
    """
    批量命令指定目录下面的文件名
    :param directory: 文件目录
    :param prefix: 文件名前缀
    """
    for count, filename in enumerate(os.listdir(directory)):
        ext = os.path.splitext(filename)[1]
        new_filename = "{}_{}{}".format(prefix, str(count).zfill(3), ext)
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
# batch_filename('./dir', 'project')


def organize_files(directory):
    """
    根据文件扩展名自动整理文件夹内容
    :param directory: 文件目录
    :return:
    """
    for filename in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, filename)):
            ext = filename.split(".")[-1]
            ext_folder = os.path.join(directory, ext)
            if not os.path.exists(ext_folder):
                os.makedirs(ext_folder)
            shutil.move(os.path.join(directory, filename), os.path.join(ext_folder, filename))
# organize_files('./downloads')


def process_excel(file_path):
    """
    对 excel 数据进行清洗, 并保存成新的文件
    :param file_path:
    :return:
    """
    df = pd.read_excel(file_path)
    df.dropna(inplace=True)
    df['Processed_Column'] = df['Original_Column'] * 2
    output_path = 'processed' + file_path
    df.to_excel(output_path, index=False)
    print(f'处理完成,以保存到{output_path}')
# process_excel('./sale_data.xlsx')


def merge_csv(directory):
    """
    合并指定目录下面的所有的 .csv 文件
    :param directory: 指定的目录
    :return:
    """
    csv_files = [os.path.join(directory,file) for file in os.listdir(directory)]
    dataframe = [pd.read_csv(file) for file in csv_files]
    merged = pd.concat(dataframe, ignore_index=True).drop_duplicates()
    merged.to_csv('merged_output.csv', index=False)
    print(f'csv以合并完成, 结果以保存为 merged_output.csv');
# merge_csv('./dir')


class ChangeHandler(PatternMatchingEventHandler):

    def on_modified(self, event):
        print(f'文件被修改, {event.src_path}')

    def on_created(self, event):
        print(f'有新的文件创建, {event.src_path}')

    def on_moved(self, event):
        print(f'文件被删除, {event.src_path}')

def monitor_directory(directory):
    """
    监听指定目录下面的文件变更
    :param directory: 目录名称
    :return:
    """
    observer = Observer()
    handler = ChangeHandler()
    observer.schedule(ChangeHandler(), directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    # observer.stop()
# monitor_directory('./workspace')


def qrcode_gen(url):
    import qrcode
    # 创建二维码实例
    qr = qrcode.QRCode(
        version=1,  # 控制二维码的大小，范围1-40
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 错误纠正等级
        box_size=10,  # 每个小方格的像素大小
        border=4,  # 边框的厚度（最小值为4）
    )
    # 添加数据到二维码
    qr.add_data(url)
    qr.make(fit=True)

    # 创建一个图片实例
    img = qr.make_image(fill='black', back_color='white')

    # 保存二维码图片
    img.save("qrcode.png")

    # 或者直接展示二维码
    img.show()


def image2_base64(file_path: str | bytes):
    import base64
    if isinstance(file_path, str):
        with open(file_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            return base64_data
    else:
        base64_data = base64.b64encode(file_path).decode('utf-8')
        return base64_data


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    batch_filename('./dir', 'project')

