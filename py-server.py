import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import socket


class HTTPServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python HTTP Server")
        self.root.geometry("800x600")

        self.server_thread = None
        self.httpd = None
        self.server_running = False

        # 端口号输入
        self.port_label = tk.Label(root, text="端口号:")
        self.port_label.pack(pady=(20, 5))

        self.port_entry = tk.Entry(root)
        self.port_entry.pack()
        self.port_entry.insert(0, "8000")  # 默认端口

        # 目录选择
        self.dir_label = tk.Label(root, text="服务目录:")
        self.dir_label.pack(pady=(20, 5))

        self.dir_entry = tk.Entry(root, width=40)
        self.dir_entry.pack()

        self.browse_button = tk.Button(root, text="浏览...", command=self.browse_directory)
        self.browse_button.pack(pady=5)

        # 控制按钮
        self.start_button = tk.Button(root, text="启动服务器", command=self.start_server)
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(root, text="停止服务器", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack()

        # 状态显示
        self.status_label = tk.Label(root, text="服务器状态: 未运行", fg="red")
        self.status_label.pack(pady=10)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def start_server(self):
        port = self.port_entry.get()
        directory = self.dir_entry.get()

        if not port.isdigit():
            messagebox.showerror("错误", "请输入有效的端口号")
            return

        port = int(port)
        if port < 1 or port > 65535:
            messagebox.showerror("错误", "端口号必须在1-65535之间")
            return

        if not directory or not os.path.isdir(directory):
            messagebox.showerror("错误", "请选择有效的目录")
            return

        # 检查端口是否可用
        if not self.is_port_available(port):
            messagebox.showerror("错误", f"端口 {port} 已被占用，请选择其他端口")
            return

        # 在后台线程中启动服务器
        self.server_thread = threading.Thread(
            target=self.run_server,
            args=(directory, port),
            daemon=True
        )
        self.server_thread.start()

        self.server_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text=f"服务器状态: 运行中 (端口: {port})", fg="green")

        # 在默认浏览器中打开
        webbrowser.open(f"http://localhost:{port}")

    def is_port_available(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return True
            except socket.error:
                return False

    def run_server(self, directory, port):
        os.chdir(directory)
        handler = SimpleHTTPRequestHandler
        self.httpd = HTTPServer(('', port), handler)

        try:
            self.httpd.serve_forever()
        except Exception as e:
            if self.server_running:  # 只有非正常停止才显示错误
                messagebox.showerror("服务器错误", str(e))
        finally:
            self.server_running = False
            self.root.after(100, self.update_ui_stopped)

    def stop_server(self):
        if self.httpd:
            # 创建一个新线程来关闭服务器，避免阻塞GUI
            stop_thread = threading.Thread(
                target=self.shutdown_server,
                daemon=True
            )
            stop_thread.start()

    def shutdown_server(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None
            self.root.after(100, self.update_ui_stopped)

    def update_ui_stopped(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="服务器状态: 未运行", fg="red")

    def on_closing(self):
        if self.server_running:
            self.stop_server()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = HTTPServerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()