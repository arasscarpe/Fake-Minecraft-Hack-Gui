import sys
import psutil
from tkinter import *
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QFrame, 
                             QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QPoint
from PyQt5.QtGui import QFont, QColor

class ClientState(QObject):
    module_changed = pyqtSignal(str, bool)
    def __init__(self):
        super().__init__()
        self.active_modules = {"HUD": False}

state = ClientState()

class VertexLoader:
    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.geometry("400x280")
        self.root.configure(bg='#0f0f0f')
        
        x = (self.root.winfo_screenwidth() // 2) - 200
        y = (self.root.winfo_screenheight() // 2) - 140
        self.root.geometry(f"+{x}+{y}")

        self.main_f = Frame(self.root, bg='#0f0f0f', highlightbackground="#333", highlightthickness=1)
        self.main_f.pack(fill=BOTH, expand=True)

        self.header = Frame(self.main_f, bg='#1a1a1a', height=40)
        self.header.pack(fill=X)
        Label(self.header, text="YourClient v2.6", fg="white", bg='#1a1a1a', font=("Segoe UI", 9)).pack(side=LEFT, padx=10) # CHANGE NAME
        
        Label(self.main_f, text="Y O U R C L I E N T", fg="#55FFFF", bg='#0f0f0f', font=("Impact", 28)).pack(pady=20) # CHANGE NAME
        
        self.status_lbl = Label(self.main_f, text="WAITING FOR PROCESS...", fg="#ff5555", bg='#0f0f0f', font=("Segoe UI", 9, "bold"))
        self.status_lbl.pack()

        self.inject_btn = Button(self.main_f, text="INJECT", state="disabled", command=self.start_injection,
                                 bg="#222", fg="#55FFFF", font=("Segoe UI", 12, "bold"), bd=0, width=15, cursor="hand2")
        self.inject_btn.pack(pady=25)

        self.check_minecraft()
        self.root.mainloop()

    def check_minecraft(self):
        found = any("javaw.exe" in p.info['name'] or "Minecraft" in p.info['name'] for p in psutil.process_iter(['name']))
        if found:
            self.status_lbl.config(text="FOUND PROCESS", fg="#55ff55")
            self.inject_btn.config(state="normal", bg="#004444")
        else:
            self.status_lbl.config(text="WAITING FOR PROCESS...", fg="#ff5555")
            self.inject_btn.config(state="disabled", bg="#222")
        self.root.after(2000, self.check_minecraft)

    def start_injection(self):
        self.inject_btn.config(text="INJECTING...", state="disabled")
        self.root.after(1000, self.launch_gui)

    def launch_gui(self):
        self.root.destroy()
        run_main_app()

class ActiveHUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(1650, 40, 250, 1000)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        
        self.labels = {}
        state.module_changed.connect(self.update_display)

    def update_display(self, name, is_active):
        hud_master = state.active_modules.get("HUD", False)
        
        if name == "HUD":
            if is_active: self.show()
            else: self.hide()

        if is_active:
            if name not in self.labels and name != "HUD":
                lbl = QLabel(name.upper())
                lbl.setFont(QFont("Segoe UI Black", 9))
                lbl.setStyleSheet("background-color: rgba(0, 0, 0, 180); color: #55FFFF; padding: 4px 12px; border-right: 4px solid #55FFFF;")
                lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.layout.addWidget(lbl)
                self.labels[name] = lbl
            if name in self.labels: self.labels[name].setVisible(hud_master)
        else:
            if name in self.labels:
                self.labels[name].hide()

class ToggleSwitch(QCheckBox):
    def __init__(self, name):
        super().__init__()
        self.name = name.upper()
        self.setFixedSize(30, 16)
        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(self.sync)

    def sync(self):
        state.active_modules[self.name] = self.isChecked()
        state.module_changed.emit(self.name, self.isChecked())

    def paintEvent(self, e):
        from PyQt5.QtGui import QPainter, QBrush
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        bg = QColor("#55AAFF") if self.isChecked() else QColor("#444444")
        p.setPen(Qt.NoPen); p.setBrush(QBrush(bg))
        p.drawRoundedRect(0, 0, 30, 16, 8, 8)
        p.setBrush(QBrush(QColor("white")))
        p.drawEllipse(16 if self.isChecked() else 2, 2, 12, 12)

class DraggablePanel(QFrame):
    def __init__(self, title, items, parent=None):
        super().__init__(parent)
        self.dragging = False
        self.offset = QPoint()
        self.setFixedWidth(200)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.container = QFrame()
        self.container.setStyleSheet("background-color: rgba(15, 15, 15, 245); border-radius: 5px; border: 1px solid #333;")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        self.main_layout.addWidget(self.container)

        self.header_frame = QFrame()
        self.header_frame.setFixedHeight(40)
        self.h_layout = QHBoxLayout(self.header_frame)
        self.title_lbl = QLabel(title.upper())
        self.title_lbl.setFont(QFont("Segoe UI Black", 10))
        self.title_lbl.setStyleSheet("color: #55FFFF; border: none; padding-left: 10px;")
        self.h_layout.addWidget(self.title_lbl)
        self.container_layout.addWidget(self.header_frame)

        self.content_w = QWidget()
        self.content_layout = QVBoxLayout(self.content_w)
        self.content_layout.setContentsMargins(10, 5, 10, 10)
        self.content_layout.setSpacing(8)

        for item in items:
            row = QHBoxLayout()
            lbl = QLabel(item.upper())
            lbl.setFont(QFont("Segoe UI", 7, QFont.Bold))
            lbl.setStyleSheet("color: #DDD; border: none;")
            row.addWidget(lbl); row.addStretch(); row.addWidget(ToggleSwitch(item))
            self.content_layout.addLayout(row)
        
        self.container_layout.addWidget(self.content_w)

    def mouseDoubleClickEvent(self, event):
        if self.header_frame.geometry().contains(event.pos()):
            is_visible = self.content_w.isVisible()
            self.content_w.setVisible(not is_visible)
            if is_visible: self.setFixedHeight(40)
            else: 
                self.setMinimumHeight(100); self.setMaximumHeight(1000)
                self.adjustSize()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True; self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging: self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event): self.dragging = False

class CheatMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 1920, 1080)

        self.data = {
            "COMBAT": ["Anchor Macro", "Auto Crystal", "Auto Hit Crystal", "Auto Inv Totem", "Auto Totem", "Crystal Optimizer", "Hitbox", "Mace Swap", "No Hit Delay", "Triger Bot"],
            "MISC": ["Auto Eat", "Auto Firework", "Auto Log", "Auto Mine", "Auto Tool", "Fast Place", "Freecam", "Sprint"],
            "DONUT": ["Anti Trap", "Auction Sniper", "Auto Sell", "Auto Spawner Sell", "Netherite Finder", "RTP Base Finder", "Spawner Protect"],
            "RENDER": ["Fullbright", "HUD", "Player ESP", "Storage ESP", "Target HUD", "Real Hitbox", "Chunk Finder"],
            "CLIENT": ["YourClient+", "Self Destruct", "Friends", "Discord Presence"] # CHANGE NAME
        }

        x = 50
        for cat, items in self.data.items():
            p = DraggablePanel(cat, items, self)
            p.move(x, 100); x += 220

class VertexOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.menu = CheatMenu()
        self.hud = ActiveHUD()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(20, 20, 250, 25) # WIDTH ADJUSTED
        
        bg = QFrame(self); bg.setGeometry(0,0,250,25)
        bg.setStyleSheet("background: rgba(255,255,255,140); border-radius: 2px;")
        btn = QPushButton("POWERED BY YOURCLIENT", bg) # CHANGE NAME
        btn.setGeometry(0,0,250,25); btn.setFont(QFont("Segoe UI", 7, QFont.Bold))
        btn.setStyleSheet("color: black; border: none; background: transparent;")
        btn.clicked.connect(lambda: self.menu.show() if not self.menu.isVisible() else self.menu.hide())
        self.show()

def run_main_app():
    app = QApplication(sys.argv)
    ex = VertexOverlay()
    sys.exit(app.exec_())

if __name__ == '__main__':
    VertexLoader()