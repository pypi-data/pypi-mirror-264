import darkdetect
import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Darkdetect Listener Example")
        self.setGeometry(300, 300, 300, 300)

        self.show()

    def on_dark_mode_changed(self, dark_mode):
        if dark_mode:
            self.setStyleSheet("background-color: black; color: white;")
        else:
            self.setStyleSheet("background-color: white; color: black;")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    listener = darkdetect.Listener(print)
    t = threading.Thread(target=listener.listen, daemon=True)
    # OR: t = threading.Thread(target=darkdetect.listener, args=(print,), daemon=True)
    t.start()
    example = Example()
    sys.exit(app.exec_())
