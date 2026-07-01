#!/usr/bin/env python
"""kohya SDXL LoRA 訓練 GUI (PySide6) -- 獨立桌面工具,不碰 WCopilot。

填參數 -> 開始訓練(QProcess 跑 accelerate launch sdxl_train_network.py)-> 即時 log/
進度 -> 可停。進度解析依 kohya 源碼真相:tqdm 用 '\\r' 覆寫、postfix key 是 avr_loss、
tqdm 走 stderr 而 epoch 行走 stdout(故 MergedChannels);停止用 taskkill /T /F 殺整個
accelerate->python tree(否則孤兒 python 繼續鎖 VRAM)。

跑法:  D:\\Work\\sd-scripts\\.venv\\Scripts\\python.exe train_gui.py
       (該 venv 需先 `pip install PySide6`;訓練本身用同 venv 的 torch cu128)
"""
import json
import os
import re
import shutil
import sys
import time

from PySide6.QtCore import QProcess, QProcessEnvironment
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QFrame, QGraphicsDropShadowEffect,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox,
    QProgressBar, QPushButton, QScrollArea, QTextEdit, QVBoxLayout, QWidget,
)

SDSCRIPTS = r"D:\Work\sd-scripts"
ACCELERATE = os.path.join(SDSCRIPTS, ".venv", "Scripts", "accelerate.exe")
TRAIN_SCRIPT = "sdxl_train_network.py"
LORAS_DIR = r"D:\Models\diffusion\loras"
HERE = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(HERE, "train_gui_settings.json")

# --- 科技感樣式(參照 examtoppt / ppt_splitter 的 design tokens) ---
C_BG = "#0B0F14"
C_CARD = "rgba(21,30,43,0.80)"
C_BORDER = "#1F2A3A"
C_PRIMARY = "#007AFF"
C_NEON = "#00BFFF"
C_TEXT = "#E6F1FF"
C_TEXT2 = "#8B9BB3"
C_MUTED = "#55657A"

QSS = f"""
QWidget {{ background:{C_BG}; color:{C_TEXT}; font-family:'Inter','Segoe UI','Microsoft JhengHei'; font-size:14px; }}
QScrollArea {{ background:transparent; border:none; }}
QLabel {{ background:transparent; }}
QLabel#h1 {{ font-size:22px; font-weight:700; color:{C_TEXT}; letter-spacing:1px; }}
QLabel#sub {{ font-size:12px; color:{C_TEXT2}; }}
QLabel#field {{ font-size:11px; color:{C_TEXT2}; font-weight:500; }}
QLineEdit, QComboBox {{ background:{C_BG}; border:1px solid {C_BORDER}; border-radius:10px; padding:7px 11px; color:{C_TEXT}; font-size:13px; min-height:16px; }}
QLineEdit:focus, QComboBox:focus {{ border:1px solid {C_NEON}; }}
QComboBox::drop-down {{ border:none; width:24px; }}
QComboBox QAbstractItemView {{ background:#151E2B; border:1px solid {C_BORDER}; border-radius:8px; selection-background-color:{C_PRIMARY}; selection-color:#FFFFFF; outline:none; }}
QFrame#card {{ background:{C_CARD}; border:1px solid {C_BORDER}; border-radius:16px; }}
QLabel#cardtitle {{ font-size:13px; font-weight:600; color:{C_NEON}; letter-spacing:1px; }}
QLabel#hint {{ font-size:12px; color:{C_MUTED}; }}
QLabel#warn {{ font-size:12px; color:#D8A657; font-weight:500; }}
QLabel#err {{ font-size:12px; color:#E24B4A; font-weight:500; }}
QPushButton#toggle {{ background:#151E2B; border:1px solid {C_BORDER}; border-radius:12px; padding:10px 14px; color:{C_TEXT2}; font-size:13px; font-weight:600; text-align:left; }}
QPushButton#toggle:hover {{ border:1px solid {C_NEON}; color:{C_NEON}; }}
QPushButton#toggle:checked {{ background:rgba(0,122,255,0.16); border:1px solid {C_NEON}; color:{C_NEON}; }}
QPushButton {{ background:#151E2B; border:1px solid {C_BORDER}; border-radius:12px; padding:9px 16px; color:{C_TEXT}; font-size:13px; }}
QPushButton:hover {{ background:rgba(0,191,255,0.10); border:1px solid {C_NEON}; color:{C_NEON}; }}
QPushButton:disabled {{ background:#151E2B; color:{C_MUTED}; border:1px solid {C_BORDER}; }}
QPushButton#primary {{ background:{C_PRIMARY}; color:#FFFFFF; border:none; border-radius:12px; padding:11px; font-size:16px; font-weight:600; letter-spacing:1px; }}
QPushButton#primary:hover {{ background:{C_NEON}; }}
QPushButton#primary:pressed {{ background:#005FD1; }}
QPushButton#primary:disabled {{ background:#1F2A3A; color:{C_MUTED}; }}
QProgressBar {{ background:{C_BG}; border:1px solid {C_BORDER}; border-radius:10px; text-align:center; height:22px; color:{C_TEXT}; font-weight:600; }}
QProgressBar::chunk {{ background:qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 {C_PRIMARY}, stop:1 {C_NEON}); border-radius:9px; }}
QTextEdit {{ background:{C_BG}; border:1px solid {C_BORDER}; border-radius:10px; color:{C_TEXT2}; font-family:'Consolas','monospace'; font-size:11px; }}
QScrollBar:vertical {{ background:transparent; width:8px; margin:2px; }}
QScrollBar::handle:vertical {{ background:{C_BORDER}; border-radius:4px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height:0; }}
"""


def glow(widget, color=C_NEON, blur=36, alpha=40):
    """Neon glow(QSS 無 box-shadow → 用 DropShadowEffect 模擬),參照 examtoppt。"""
    eff = QGraphicsDropShadowEffect(widget)
    eff.setBlurRadius(blur)
    c = QColor(color)
    c.setAlpha(alpha)
    eff.setColor(c)
    eff.setOffset(0, 0)
    widget.setGraphicsEffect(eff)


DEFAULTS = {
    "base_ckpt": r"D:\Models\diffusion\checkpoints\waiIllustriousSDXL_v170.safetensors",
    "dataset_root": r"D:\Work\lora-training\wnboy",
    "output_name": "wnboy_v170",
    "dim": "32", "alpha": "16", "batch": "2", "epochs": "10",
    "lr": "1e-4", "resolution": "1024",
    "unet_lr": "1e-4", "te_lr": "5e-5", "optimizer": "AdamW8bit",
    "scheduler": "cosine", "clip_skip": "2", "min_snr": "5",
    "save_every": "1", "seed": "42", "min_bucket": "512", "max_bucket": "1536",
}

ILLEGAL = re.compile(r'[<>:"/\\|?*]')
REPEAT_DIR = re.compile(r"^\d+_.+")
AVR_LOSS = re.compile(r"avr_loss=([0-9.]+)")
EPOCH_RE = re.compile(r"epoch\s+(\d+)\s*/\s*(\d+)")
STEPS_RE = re.compile(r"steps:\s*\d+%.*?(\d+)\s*/\s*(\d+)")

ADV_FIELDS = [
    ("optimizer", "optimizer_type"), ("scheduler", "lr_scheduler"),
    ("unet_lr", "unet_lr"), ("te_lr", "text_encoder_lr"), ("clip_skip", "clip_skip"),
    ("min_snr", "min_snr_gamma"), ("save_every", "save_every_n_epochs"), ("seed", "seed"),
    ("min_bucket", "min_bucket_reso"), ("max_bucket", "max_bucket_reso"),
]


class TrainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("kohya SDXL LoRA 訓練")
        self.resize(720, 780)
        self.proc = None
        self._buf = b""
        self._log_throttle = 0
        self._start_time = 0.0
        self.cur_epoch = 0
        self.tot_epoch = 0
        self.fields = {}

        content = QWidget()
        root = QVBoxLayout(content)
        root.setContentsMargins(28, 18, 28, 18)
        root.setSpacing(8)

        title = QLabel("kohya SDXL LoRA 訓練")
        title.setObjectName("h1")
        sub = QLabel("獨立桌面工具 · 終端機跳視窗 · 不碰 WCopilot")
        sub.setObjectName("sub")
        root.addWidget(title)
        root.addWidget(sub)

        # ---- Card 1:路徑與資料集 ----
        c1, l1 = self._card("📁  路徑與資料集")
        self.base_ckpt = QLineEdit()
        l1.addWidget(self._field("📄 底模 checkpoint(.safetensors)"))
        l1.addLayout(self._prow(self.base_ckpt, self._pick_ckpt))
        self.dataset_root = QLineEdit()
        l1.addWidget(self._field("📂 資料集 root"))
        l1.addLayout(self._prow(self.dataset_root, self._pick_dataset))
        l1.addWidget(self._hint("root 內含 img\\<repeats>_<trigger>\\,例 img\\10_wnboy\\"))
        self.output_name = QLineEdit()
        l1.addWidget(self._field("✏️ LoRA 名稱"))
        l1.addWidget(self.output_name)
        root.addWidget(c1)

        # ---- Card 2:訓練參數 ----
        c2, l2 = self._card("⚙️  訓練參數")
        grid = QGridLayout()
        grid.setSpacing(8)
        for key, label, r, c in [("dim", "network dim", 0, 0), ("alpha", "alpha", 0, 1),
                                 ("batch", "batch", 0, 2), ("epochs", "epochs", 0, 3),
                                 ("lr", "learning rate", 1, 0), ("resolution", "解析度", 1, 1)]:
            le = QLineEdit()
            self.fields[key] = le
            cell = QVBoxLayout()
            cell.setSpacing(3)
            cell.addWidget(self._field(label))
            cell.addWidget(le)
            holder = QWidget()
            holder.setLayout(cell)
            grid.addWidget(holder, r, c)
        l2.addLayout(grid)

        self.adv_btn = self._toggle("▸ 進階(wnboy 驗證過的預設,點開調)")
        l2.addWidget(self.adv_btn)
        self.adv_box = QWidget()
        adv_grid = QGridLayout(self.adv_box)
        adv_grid.setContentsMargins(0, 4, 0, 0)
        adv_grid.setSpacing(8)
        for i, (k, lbl) in enumerate(ADV_FIELDS):
            le = QLineEdit()
            self.fields[k] = le
            cell = QVBoxLayout()
            cell.setSpacing(3)
            cell.addWidget(self._field(lbl))
            cell.addWidget(le)
            holder = QWidget()
            holder.setLayout(cell)
            adv_grid.addWidget(holder, i // 2, i % 2)
        l2.addWidget(self.adv_box)
        self.adv_box.setVisible(False)
        self.adv_btn.toggled.connect(self._toggle_adv)
        root.addWidget(c2)

        # ---- Card 3:執行 ----
        c3, l3 = self._card("🚀  執行")
        warn = QLabel("⚠ 訓練吃滿 GPU,期間 ComfyUI / 其他 GPU 工作會卡到訓練結束。")
        warn.setObjectName("warn")
        warn.setWordWrap(True)
        l3.addWidget(warn)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.start_btn = QPushButton("開始訓練")
        self.start_btn.setObjectName("primary")
        self.start_btn.clicked.connect(self._start)
        glow(self.start_btn)
        self.stop_btn = QPushButton("停止")
        self.stop_btn.setObjectName("sec")
        self.stop_btn.clicked.connect(self._stop)
        self.stop_btn.setEnabled(False)
        btn_row.addWidget(self.start_btn, 1)
        btn_row.addWidget(self.stop_btn)
        l3.addLayout(btn_row)

        self.err_lbl = QLabel("")
        self.err_lbl.setObjectName("err")
        self.err_lbl.setWordWrap(True)
        l3.addWidget(self.err_lbl)

        self.prog_lbl = QLabel("尚未開始")
        self.prog_lbl.setObjectName("hint")
        l3.addWidget(self.prog_lbl)
        self.prog_bar = QProgressBar()
        self.prog_bar.setRange(0, 100)
        l3.addWidget(self.prog_bar)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        l3.addWidget(self.log, 1)

        post_row = QHBoxLayout()
        post_row.setSpacing(8)
        self.epoch_combo = QComboBox()
        self.copy_btn = QPushButton("複製選定 epoch 到 loras")
        self.copy_btn.setObjectName("sec")
        self.copy_btn.clicked.connect(self._copy_to_loras)
        self.copy_btn.setEnabled(False)
        post_row.addWidget(self.epoch_combo, 1)
        post_row.addWidget(self.copy_btn)
        l3.addLayout(post_row)
        root.addWidget(c3, 1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(content)
        self.setCentralWidget(scroll)

        self._load_settings()

    def _card(self, title):
        card = QFrame()
        card.setObjectName("card")
        glow(card, blur=44, alpha=36)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 9, 16, 9)
        lay.setSpacing(6)
        t = QLabel(title)
        t.setObjectName("cardtitle")
        lay.addWidget(t)
        return card, lay

    def _field(self, t):
        lbl = QLabel(t)
        lbl.setObjectName("field")
        return lbl

    def _hint(self, t):
        lbl = QLabel(t)
        lbl.setObjectName("hint")
        lbl.setWordWrap(True)
        return lbl

    def _prow(self, le, pick):
        row = QHBoxLayout()
        row.setSpacing(8)
        btn = QPushButton("📂 選")
        btn.setObjectName("sec")
        btn.clicked.connect(pick)
        row.addWidget(le, 1)
        row.addWidget(btn)
        return row

    def _toggle(self, text, checked=False):
        b = QPushButton(text)
        b.setObjectName("toggle")
        b.setCheckable(True)
        b.setChecked(checked)
        return b

    def _toggle_adv(self, on):
        self.adv_box.setVisible(on)
        self.adv_btn.setText(("▾ " if on else "▸ ") + "進階(wnboy 驗證過的預設,點開調)")

    def _pick_ckpt(self):
        start = os.path.dirname(self.base_ckpt.text()) or r"D:\Models\diffusion\checkpoints"
        p, _ = QFileDialog.getOpenFileName(self, "選底模", start, "Safetensors (*.safetensors)")
        if p:
            self.base_ckpt.setText(p.replace("/", "\\"))

    def _pick_dataset(self):
        p = QFileDialog.getExistingDirectory(self, "選資料集 root", self.dataset_root.text() or r"D:\Work\lora-training")
        if p:
            self.dataset_root.setText(p.replace("/", "\\"))

    def _vals(self):
        v = {"base_ckpt": self.base_ckpt.text().strip(),
             "dataset_root": self.dataset_root.text().strip(),
             "output_name": self.output_name.text().strip()}
        for k, le in self.fields.items():
            v[k] = le.text().strip()
        return v

    def _load_settings(self):
        data = dict(DEFAULTS)
        try:
            with open(SETTINGS_PATH, encoding="utf-8") as f:
                data.update(json.load(f))
        except Exception:
            pass
        self.base_ckpt.setText(data.get("base_ckpt", ""))
        self.dataset_root.setText(data.get("dataset_root", ""))
        self.output_name.setText(data.get("output_name", ""))
        for k, le in self.fields.items():
            le.setText(str(data.get(k, DEFAULTS.get(k, ""))))

    def _save_settings(self):
        try:
            with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump(self._vals(), f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def _validate(self, v):
        if not (os.path.isfile(v["base_ckpt"]) and v["base_ckpt"].lower().endswith(".safetensors")):
            return "底模不存在或不是 .safetensors"
        root = v["dataset_root"]
        img = os.path.join(root, "img")
        if not os.path.isdir(root) or not os.path.isdir(img):
            return "資料集 root 不存在或缺 img\\ 子目錄"
        subs = [d for d in os.listdir(img) if os.path.isdir(os.path.join(img, d)) and REPEAT_DIR.match(d)]
        if not subs:
            return "img\\ 底下找不到 <repeats>_<trigger> 子夾(例 10_wnboy),kohya 會訓 0 張"
        if not v["output_name"] or ILLEGAL.search(v["output_name"]):
            return "LoRA 名稱空或含非法字元 <>:\"/\\|?*"
        for k in ("dim", "alpha", "batch", "epochs", "clip_skip", "min_snr", "save_every", "seed", "min_bucket", "max_bucket", "resolution"):
            try:
                int(v[k])
            except Exception:
                return "%s 要整數" % k
        for k in ("lr", "unet_lr", "te_lr"):
            try:
                float(v[k])
            except Exception:
                return "%s 要數字" % k
        if not os.path.isfile(ACCELERATE) or not os.path.isfile(os.path.join(SDSCRIPTS, TRAIN_SCRIPT)):
            return "找不到 accelerate.exe 或 sdxl_train_network.py(檢查 sd-scripts 路徑)"
        return None

    def _build_args(self, v):
        root = v["dataset_root"]
        res = v["resolution"]
        return [
            "launch", "--num_processes=1", "--mixed_precision=bf16", "--dynamo_backend=no",
            TRAIN_SCRIPT,
            "--pretrained_model_name_or_path=%s" % v["base_ckpt"],
            "--train_data_dir=%s" % os.path.join(root, "img"),
            "--output_dir=%s" % os.path.join(root, "output"),
            "--output_name=%s" % v["output_name"],
            "--logging_dir=%s" % os.path.join(root, "log"),
            "--network_module=networks.lora",
            "--network_dim=%s" % v["dim"], "--network_alpha=%s" % v["alpha"],
            "--resolution=%s,%s" % (res, res),
            "--enable_bucket", "--min_bucket_reso=%s" % v["min_bucket"],
            "--max_bucket_reso=%s" % v["max_bucket"], "--bucket_no_upscale",
            "--train_batch_size=%s" % v["batch"], "--max_train_epochs=%s" % v["epochs"],
            "--save_every_n_epochs=%s" % v["save_every"], "--save_model_as=safetensors",
            "--learning_rate=%s" % v["lr"], "--unet_lr=%s" % v["unet_lr"],
            "--text_encoder_lr=%s" % v["te_lr"], "--optimizer_type=%s" % v["optimizer"],
            "--lr_scheduler=%s" % v["scheduler"], "--mixed_precision=bf16", "--save_precision=bf16",
            "--sdpa", "--gradient_checkpointing", "--cache_latents",
            "--clip_skip=%s" % v["clip_skip"], "--max_token_length=225",
            "--caption_extension=.txt", "--min_snr_gamma=%s" % v["min_snr"],
            "--no_half_vae", "--seed=%s" % v["seed"],
        ]

    def _start(self):
        v = self._vals()
        err = self._validate(v)
        if err:
            self.err_lbl.setText("✗ " + err)
            return
        self.err_lbl.setText("")
        self._save_settings()
        args = self._build_args(v)
        self.tot_epoch = int(v["epochs"])
        self.cur_epoch = 0
        self._buf = b""
        self._log_throttle = 0
        self.log.clear()
        self.log.append("$ accelerate " + " ".join(args[1:]) + "\n")
        self.prog_bar.setRange(0, 0)
        self.prog_lbl.setText("啟動中(載入模型 / cache latents)...")
        self.epoch_combo.clear()
        self.copy_btn.setEnabled(False)

        self.proc = QProcess(self)
        self.proc.setWorkingDirectory(SDSCRIPTS)
        self.proc.setProgram(ACCELERATE)
        self.proc.setArguments(args)
        env = QProcessEnvironment.systemEnvironment()
        env.insert("PYTHONUTF8", "1")
        env.insert("PYTHONIOENCODING", "utf-8")
        self.proc.setProcessEnvironment(env)
        self.proc.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.proc.readyReadStandardOutput.connect(self._on_output)
        self.proc.finished.connect(self._on_finished)
        self.proc.errorOccurred.connect(self._on_error)
        self._start_time = time.time()
        self.proc.start()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def _stop(self):
        if self.proc and self.proc.state() != QProcess.ProcessState.NotRunning:
            pid = int(self.proc.processId())
            QProcess.startDetached("taskkill", ["/PID", str(pid), "/T", "/F"])
            self.log.append("\n[已送 taskkill /T /F,殺整個訓練 tree]\n")

    def _on_error(self, e):
        self.log.append("\n[QProcess error: %s]\n" % e)

    def _on_output(self):
        self._buf += bytes(self.proc.readAllStandardOutput())
        parts = re.split(rb"[\r\n]", self._buf)
        self._buf = parts.pop()
        for raw in parts:
            if not raw.strip():
                continue
            frag = raw.decode("utf-8", "replace")
            me = EPOCH_RE.search(frag)
            if me:
                self.cur_epoch, self.tot_epoch = int(me.group(1)), int(me.group(2))
            ms = STEPS_RE.search(frag)
            if ms:
                cur, tot = int(ms.group(1)), int(ms.group(2))
                if self.prog_bar.maximum() == 0:
                    self.prog_bar.setRange(0, tot)
                self.prog_bar.setValue(cur)
                ml = AVR_LOSS.search(frag)
                loss = (" · avg loss %s" % ml.group(1)) if ml else ""
                # kohya 的 "epoch N/total" 行在該 epoch 跑完才印(顯示會落後一輪),
                # 故從全域 step 自算當前 epoch:step 是全訓練累計,每 epoch = tot / tot_epoch 步
                disp = self.cur_epoch
                if self.tot_epoch > 0 and tot > 0:
                    spe = tot / self.tot_epoch
                    disp = self.tot_epoch if cur >= tot else min(self.tot_epoch, int(cur / spe) + 1)
                self.prog_lbl.setText("Epoch %d/%d · Step %d/%d%s" % (disp, self.tot_epoch, cur, tot, loss))
                self._log_throttle += 1
                if self._log_throttle >= 25:
                    self._log_throttle = 0
                    self.log.append(frag)
            else:
                self.log.append(frag)

    def _on_finished(self, code, status):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        if self.prog_bar.maximum() == 0:
            self.prog_bar.setRange(0, 100)
        self.prog_lbl.setText("完成(exit 0)" if code == 0 else "結束 exit %d(中止或錯誤,看 log)" % code)
        self._populate_epochs()

    def _populate_epochs(self):
        v = self._vals()
        outdir = os.path.join(v["dataset_root"], "output")
        self.epoch_combo.clear()
        try:
            files = [f for f in os.listdir(outdir)
                     if f.lower().endswith(".safetensors") and f.startswith(v["output_name"])
                     and os.path.getmtime(os.path.join(outdir, f)) >= self._start_time - 5]
            for f in sorted(files):
                self.epoch_combo.addItem(f, os.path.join(outdir, f))
            self.copy_btn.setEnabled(bool(files))
        except Exception:
            pass

    def _copy_to_loras(self):
        src = self.epoch_combo.currentData()
        if not src:
            return
        if not os.path.isdir(LORAS_DIR):
            if QMessageBox.question(self, "建目錄?", "%s 不存在,要建嗎?" % LORAS_DIR) != QMessageBox.StandardButton.Yes:
                return
            os.makedirs(LORAS_DIR, exist_ok=True)
        dst = os.path.join(LORAS_DIR, os.path.basename(src))
        if os.path.exists(dst):
            if QMessageBox.question(self, "覆寫?", "%s 已存在,覆寫?" % dst) != QMessageBox.StandardButton.Yes:
                return
        shutil.copy2(src, dst)
        self.log.append("\n[已複製到 %s]\n" % dst)

    def closeEvent(self, ev):
        if self.proc and self.proc.state() != QProcess.ProcessState.NotRunning:
            if QMessageBox.question(self, "訓練進行中", "訓練還在跑,要停止並關閉嗎?") != QMessageBox.StandardButton.Yes:
                ev.ignore()
                return
            self._stop()
        self._save_settings()
        ev.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    w = TrainGUI()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
