import tkinter as tk
import logging

class LogDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Display App")

        self.log_text = tk.Text(root)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.setup_logging()

        log_button = tk.Button(root, text="Generate Log", command=self.generate_log)
        log_button.pack()

    def setup_logging(self):
        self.log_messages = []  # 用于存储日志消息的列表

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[LogListHandler(self.log_messages)])

    def generate_log(self):
        logging.info("This is a log message")

        self.log_text.delete(1.0, tk.END)  # 清空文本框
        for message in reversed(self.log_messages):
            self.log_text.insert(tk.END, message + '\n')

class LogListHandler(logging.Handler):
    def __init__(self, log_messages):
        super().__init__()
        self.log_messages = log_messages

    def emit(self, record):
        log_message = self.format(record)
        self.log_messages.append(log_message)

if __name__ == '__main__':
    root = tk.Tk()
    app = LogDisplayApp(root)
    root.mainloop()
