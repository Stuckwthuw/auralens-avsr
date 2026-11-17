"""Auralens AVSR — Main Application Window.

This module implements the primary Tkinter user interface for the Auralens
audio-visual speech recognition (AVSR) system. Developed by TV5 (Application & UI),
it provides:
- Two operational modes:
    1. "Phụ đề tiếng Việt từ âm thanh" (Free ASR speech-to-text)
    2. "Thí nghiệm 10 câu nghe–nhìn" (10-sentence Audio-Visual experiment)
- Start/Stop toggle button ("Bắt đầu" / "Dừng")
- High-contrast, large-font Vietnamese subtitle display area
- Real-time status indicator ("Sẵn sàng", "Đang thu...", "Đang xử lý...",
  "Chưa nhận dạng rõ", "Lỗi")
- Subtitle font size control (16 - 48 pt)
- High contrast light/dark mode switcher
- Source selector for experiment mode (A / V / AV)
- Thread-safe architecture via queue.Queue and root.after()
- Live capture through a single Recorder owner (camera + microphone)
- Device label fed by real device_info, released on stop and on window close
- Mock data simulation with prominent "⚠ Mô phỏng" badge
"""

from __future__ import annotations

import logging
import queue
import random
import threading
import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

# Mode Definitions (MUST have distinct names)
MODE_ASR_FREE: str = "Phụ đề tiếng Việt từ âm thanh"
MODE_EXPERIMENT_10: str = "Thí nghiệm 10 câu nghe–nhìn"

# Source Options for Experiment Mode
SOURCE_AUDIO: str = "A"
SOURCE_VISUAL: str = "V"
SOURCE_AV: str = "AV"

# Status Constants
STATUS_READY: str = "Sẵn sàng"
STATUS_RECORDING: str = "Đang thu..."
STATUS_PROCESSING: str = "Đang xử lý..."
STATUS_UNCERTAIN: str = "Chưa nhận dạng rõ"
STATUS_ERROR: str = "Lỗi"

# The 10 predefined sentences defined by TV1 contract (c00 - c09)
PREDEFINED_10_SENTENCES: List[str] = [
    "Xin chào bạn.",
    "Bạn tên là gì?",
    "Tôi cần giúp đỡ.",
    "Bạn nói lại được không?",
    "Xin nói chậm hơn.",
    "Cảm ơn bạn rất nhiều.",
    "Tôi chưa hiểu ý bạn.",
    "Chúng ta gặp nhau ở đâu?",
    "Bây giờ là mấy giờ?",
    "Hẹn gặp lại bạn.",
]

# Uncertain / unclassified result for experiment mode
UNCERTAIN_EXPERIMENT_TEXT: str = "Chưa nhận dạng được"

# Mock examples in Vietnamese with diacritics for free ASR mode
MOCK_ASR_SENTENCES: List[str] = [
    "Xin chào, tôi là sinh viên năm ba.",
    "Hôm nay thời tiết đẹp quá.",
    "Hệ thống Auralens hỗ trợ phụ đề tiếng Việt thông minh.",
    "Kính thực tế tăng cường hiển thị phụ đề trực quan.",
    "Bạn có thể điều chỉnh kích thước phụ đề dễ dàng.",
    "Nhận dạng giọng nói kết hợp khẩu hình giúp giảm nhiễu.",
    "Công nghệ nghe–nhìn hỗ trợ người khiếm thính giao tiếp.",
    "Âm thanh thu được rất rõ ràng và chuẩn xác.",
]

# Theme Color Palettes
THEME_DARK: Dict[str, str] = {
    "bg_root": "#121214",
    "bg_card": "#1c1d22",
    "bg_subtitle": "#000000",
    "fg_subtitle": "#ffffff",
    "fg_text": "#f3f4f6",
    "fg_subtext": "#9ca3af",
    "border": "#2e3138",
    "control_bg": "#252730",
    "btn_bg": "#2e323e",
    "btn_fg": "#ffffff",
    "btn_active": "#3f4454",
    "start_btn_bg": "#15803d",
    "stop_btn_bg": "#b91c1c",
    "status_bar_bg": "#18191e",
    "mock_badge_bg": "#854d0e",
    "mock_badge_fg": "#fef08a",
    "real_badge_bg": "#14532d",
    "real_badge_fg": "#86efac",
}

THEME_LIGHT: Dict[str, str] = {
    "bg_root": "#f4f5f8",
    "bg_card": "#ffffff",
    "bg_subtitle": "#ffffff",
    "fg_subtitle": "#000000",
    "fg_text": "#111827",
    "fg_subtext": "#4b5563",
    "border": "#d1d5db",
    "control_bg": "#e5e7eb",
    "btn_bg": "#e2e8f0",
    "btn_fg": "#0f172a",
    "btn_active": "#cbd5e1",
    "start_btn_bg": "#16a34a",
    "stop_btn_bg": "#dc2626",
    "status_bar_bg": "#e2e8f0",
    "mock_badge_bg": "#fef08a",
    "mock_badge_fg": "#854d0e",
    "real_badge_bg": "#dcfce7",
    "real_badge_fg": "#166534",
}

# Status Indicator Colors
STATUS_COLORS: Dict[str, Dict[str, Tuple[str, str]]] = {
    # status: {"light": (bg, fg), "dark": (bg, fg)}
    STATUS_READY: {
        "light": ("#e2e8f0", "#475569"),
        "dark": ("#334155", "#cbd5e1"),
    },
    STATUS_RECORDING: {
        "light": ("#fee2e2", "#b91c1c"),
        "dark": ("#7f1d1d", "#fca5a5"),
    },
    STATUS_PROCESSING: {
        "light": ("#ffedd5", "#c2410c"),
        "dark": ("#7c2d12", "#fed7aa"),
    },
    STATUS_UNCERTAIN: {
        "light": ("#fef9c3", "#854d0e"),
        "dark": ("#713f12", "#fef08a"),
    },
    STATUS_ERROR: {
        "light": ("#dc2626", "#ffffff"),
        "dark": ("#b91c1c", "#ffffff"),
    },
}


def _tao_recorder(**kwargs: Any) -> Any:
    """Create the real Recorder lazily.

    Importing inside the factory keeps mock mode and the UI unit tests free of
    OpenCV/sounddevice, so the interface can run on a machine without a camera.
    """
    from auralens.capture.recorder import Recorder

    return Recorder(**kwargs)


class AuralensApp:
    """Tkinter application for Auralens Audio-Visual Subtitling System."""

    def __init__(
        self,
        root: Optional[tk.Tk] = None,
        mock_mode: bool = True,
        camera_index: int = 0,
        audio_device: Optional[Union[int, str]] = None,
        sample_rate: int = 16000,
        recorder_factory: Optional[Callable[..., Any]] = None,
        output_dir: Union[str, Path] = "recordings",
        max_duration_s: float = 15.0,
    ) -> None:
        """Initialize the Auralens application.

        Args:
            root: Optional Tk root instance. If None, a new tk.Tk() is created.
            mock_mode: When True, simulates speech recognition with mock data.
            camera_index: OpenCV camera index used in live mode.
            audio_device: sounddevice input index/name (None = system default).
            sample_rate: Audio sample rate in Hz (16 kHz per project contract).
            recorder_factory: Test seam; builds a Recorder-like object. Defaults
                to the real Recorder, imported only when live mode runs.
            output_dir: Root directory where live turns are saved as pilot data
                (``<output_dir>/<sample_id>/``); ``recordings/`` is gitignored.
            max_duration_s: Cap for one capture turn in seconds.
        """
        # Own or create Tk root
        if root is None:
            self.root = tk.Tk()
            self._owns_root = True
        else:
            self.root = root
            self._owns_root = False

        # Core Configuration & State
        self.mock_mode: bool = mock_mode
        self.camera_index: int = camera_index
        self.audio_device = audio_device
        self.sample_rate: int = sample_rate
        self._recorder_factory = recorder_factory or _tao_recorder
        self._recorder: Any = None
        self.output_dir = str(output_dir)
        self.max_duration_s = float(max_duration_s)
        self.dark_mode: bool = True  # High contrast dark mode by default
        self.font_size: int = 28  # Default subtitle font size (24pt+)
        self.is_running: bool = False
        self.current_status: str = STATUS_READY
        self._is_closing: bool = False

        # Thread synchronization
        self.queue: queue.Queue[Dict[str, Any]] = queue.Queue()
        self._stop_event = threading.Event()
        self._recording_done_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None

        # Choose best available font
        available_fonts = tkfont.families(self.root)
        if "Segoe UI" in available_fonts:
            self.font_family = "Segoe UI"
        elif "Arial" in available_fonts:
            self.font_family = "Arial"
        else:
            self.font_family = "Helvetica"

        # Window properties
        self.root.title("Auralens — Phụ đề thông minh")
        self.root.minsize(800, 400)
        self.root.geometry("960x560")

        # Window close handler
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Tkinter variables
        self.mode_var = tk.StringVar(value=MODE_ASR_FREE)
        self.source_var = tk.StringVar(value=SOURCE_AV)
        self.font_size_var = tk.IntVar(value=self.font_size)

        # Thread-safe cached configuration values
        self._active_mode: str = MODE_ASR_FREE
        self._active_source: str = SOURCE_AV

        # Build UI layout
        self._build_ui()

        # Apply initial theme
        self._apply_theme()

        # Start queue polling loop (100ms interval)
        self.root.after(100, self._poll_queue)

    @property
    def theme(self) -> Dict[str, str]:
        """Return the current active color palette."""
        return THEME_DARK if self.dark_mode else THEME_LIGHT

    # -------------------------------------------------------------------------
    # UI Construction
    # -------------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Create and layout all user interface widgets."""
        # Top-level container
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # 1. Header Bar: Title, Contrast Switch, Font Size Controls
        self._build_header_bar()

        # 2. Control Toolbar: Mode selector, Source selector, Start/Stop button, Status indicator
        self._build_control_bar()

        # 3. Main Subtitle Area (Center, expansive, high contrast)
        self._build_subtitle_area()

        # 4. Bottom Status Bar: Mode, Hardware status, Mock badge
        self._build_status_bar()

    def _build_header_bar(self) -> None:
        """Build the top header bar with branding and quick display settings."""
        self.header_frame = tk.Frame(self.main_container, padx=16, pady=10)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        # Left: Branding
        branding_frame = tk.Frame(self.header_frame)
        branding_frame.pack(side=tk.LEFT)
        self._branding_frame = branding_frame

        self.title_label = tk.Label(
            branding_frame,
            text="AURALENS",
            font=(self.font_family, 15, "bold"),
            anchor="w",
        )
        self.title_label.pack(side=tk.LEFT)

        self.subtitle_header_label = tk.Label(
            branding_frame,
            text=" |  Hệ thống phụ đề thông minh nghe–nhìn",
            font=(self.font_family, 11),
            anchor="w",
        )
        self.subtitle_header_label.pack(side=tk.LEFT)

        # Right: Display adjustments (Font size + Contrast toggle)
        display_frame = tk.Frame(self.header_frame)
        display_frame.pack(side=tk.RIGHT)
        self._display_frame = display_frame

        # Font size adjustment label
        self.font_label = tk.Label(
            display_frame,
            text="Cỡ chữ:",
            font=(self.font_family, 10, "bold"),
        )
        self.font_label.pack(side=tk.LEFT, padx=(0, 6))

        # Font size - button
        self.font_minus_btn = tk.Button(
            display_frame,
            text="−",
            font=(self.font_family, 11, "bold"),
            width=2,
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self._adjust_font_size(-2),
        )
        self.font_minus_btn.pack(side=tk.LEFT, padx=2)

        # Font size slider
        self.font_slider = tk.Scale(
            display_frame,
            from_=16,
            to=48,
            orient=tk.HORIZONTAL,
            variable=self.font_size_var,
            showvalue=False,
            length=100,
            command=self._on_slider_change,
            cursor="hand2",
            relief=tk.FLAT,
            highlightthickness=0,
        )
        self.font_slider.pack(side=tk.LEFT, padx=4)

        # Font size + button
        self.font_plus_btn = tk.Button(
            display_frame,
            text="+",
            font=(self.font_family, 11, "bold"),
            width=2,
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self._adjust_font_size(+2),
        )
        self.font_plus_btn.pack(side=tk.LEFT, padx=2)

        # Font size value readout
        self.font_value_label = tk.Label(
            display_frame,
            text=f"{self.font_size} pt",
            font=(self.font_family, 10),
            width=6,
        )
        self.font_value_label.pack(side=tk.LEFT, padx=(4, 16))

        # Contrast toggle button
        self.contrast_btn = tk.Button(
            display_frame,
            text="☀️ Chế độ sáng",
            font=(self.font_family, 10, "bold"),
            padx=10,
            pady=3,
            relief=tk.FLAT,
            cursor="hand2",
            command=self._toggle_contrast,
        )
        self.contrast_btn.pack(side=tk.LEFT)

    def _build_control_bar(self) -> None:
        """Build the control panel containing Mode selector, Source selector, Start/Stop button, and Status."""
        self.control_frame = tk.Frame(self.main_container, padx=16, pady=10)
        self.control_frame.pack(fill=tk.X, side=tk.TOP)

        # Mode Selection Section
        self.mode_group = tk.LabelFrame(
            self.control_frame,
            text=" Chế độ hoạt động ",
            font=(self.font_family, 10, "bold"),
            padx=12,
            pady=6,
        )
        self.mode_group.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))

        self.radio_mode_asr = tk.Radiobutton(
            self.mode_group,
            text=MODE_ASR_FREE,
            variable=self.mode_var,
            value=MODE_ASR_FREE,
            font=(self.font_family, 10),
            command=self._on_mode_change,
            cursor="hand2",
        )
        self.radio_mode_asr.pack(anchor="w", pady=1)

        self.radio_mode_exp = tk.Radiobutton(
            self.mode_group,
            text=MODE_EXPERIMENT_10,
            variable=self.mode_var,
            value=MODE_EXPERIMENT_10,
            font=(self.font_family, 10),
            command=self._on_mode_change,
            cursor="hand2",
        )
        self.radio_mode_exp.pack(anchor="w", pady=1)

        # Source Selection Section (Only visible in Experiment mode)
        self.source_group = tk.LabelFrame(
            self.control_frame,
            text=" Nguồn nhận dạng ",
            font=(self.font_family, 10, "bold"),
            padx=12,
            pady=6,
        )
        # Hidden by default because initial mode is MODE_ASR_FREE
        self.radio_source_a = tk.Radiobutton(
            self.source_group,
            text="A (Âm thanh)",
            variable=self.source_var,
            value=SOURCE_AUDIO,
            font=(self.font_family, 10),
            command=self._on_source_change,
            cursor="hand2",
        )
        self.radio_source_a.pack(side=tk.LEFT, padx=6)

        self.radio_source_v = tk.Radiobutton(
            self.source_group,
            text="V (Hình ảnh / Khẩu hình)",
            variable=self.source_var,
            value=SOURCE_VISUAL,
            font=(self.font_family, 10),
            command=self._on_source_change,
            cursor="hand2",
        )
        self.radio_source_v.pack(side=tk.LEFT, padx=6)

        self.radio_source_av = tk.Radiobutton(
            self.source_group,
            text="AV (Nghe–Nhìn)",
            variable=self.source_var,
            value=SOURCE_AV,
            font=(self.font_family, 10),
            command=self._on_source_change,
            cursor="hand2",
        )
        self.radio_source_av.pack(side=tk.LEFT, padx=6)

        # Start / Stop Toggle Button Frame
        action_frame = tk.Frame(self.control_frame)
        action_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self._action_frame = action_frame

        # Start/Stop Button
        self.start_stop_btn = tk.Button(
            action_frame,
            text="Bắt đầu",
            font=(self.font_family, 13, "bold"),
            width=12,
            height=1,
            padx=14,
            pady=6,
            relief=tk.FLAT,
            cursor="hand2",
            command=self._on_start_stop,
        )
        self.start_stop_btn.pack(side=tk.RIGHT, padx=(10, 0))

        # Status Indicator Label (Colored pill)
        self.status_indicator = tk.Label(
            action_frame,
            text=STATUS_READY,
            font=(self.font_family, 11, "bold"),
            padx=16,
            pady=8,
            relief=tk.SOLID,
            borderwidth=1,
        )
        self.status_indicator.pack(side=tk.RIGHT, padx=(0, 6))

    def _build_subtitle_area(self) -> None:
        """Build the large, prominent center subtitle area."""
        self.subtitle_outer_frame = tk.Frame(self.main_container, padx=16, pady=8)
        self.subtitle_outer_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        # Bordered Card for Subtitle Box
        self.subtitle_box = tk.Frame(
            self.subtitle_outer_frame,
            relief=tk.SOLID,
            borderwidth=2,
            padx=24,
            pady=24,
        )
        self.subtitle_box.pack(fill=tk.BOTH, expand=True)

        # Subtitle Content Label (1-2 lines, Segoe UI/Arial 24pt+)
        self.default_placeholder = "(Phụ đề tiếng Việt sẽ xuất hiện tại đây khi bắt đầu)"
        self.subtitle_label = tk.Label(
            self.subtitle_box,
            text=self.default_placeholder,
            font=(self.font_family, self.font_size, "bold"),
            justify=tk.CENTER,
            anchor="center",
            wraplength=860,
        )
        self.subtitle_label.pack(fill=tk.BOTH, expand=True)

        # Dynamic wraplength on window resize
        self.subtitle_box.bind("<Configure>", self._on_subtitle_box_resize)

        # Subtitle context hint / source tag
        self.subtitle_meta_label = tk.Label(
            self.subtitle_box,
            text="",
            font=(self.font_family, 10),
            anchor="e",
        )
        self.subtitle_meta_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(8, 0))

    def _build_status_bar(self) -> None:
        """Build the bottom status bar with mode info, device status, and mock badge."""
        self.status_bar_frame = tk.Frame(
            self.main_container,
            padx=16,
            pady=6,
            relief=tk.GROOVE,
            borderwidth=1,
        )
        self.status_bar_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Left: Current Mode
        self.status_mode_label = tk.Label(
            self.status_bar_frame,
            text=f"Chế độ: {self.mode_var.get()}",
            font=(self.font_family, 10),
            anchor="w",
        )
        self.status_mode_label.pack(side=tk.LEFT, padx=(0, 16))

        # Middle: Device Hardware Status. Text is only filled from a real
        # device query (Recorder.device_info) or a close event — never assumed.
        self.status_device_label = tk.Label(
            self.status_bar_frame,
            text="Thiết bị: chưa mở — bấm Bắt đầu",
            font=(self.font_family, 10),
            anchor="w",
        )
        self.status_device_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Right: Mock Badge (Must be prominent when mock_mode is active)
        self.mock_badge = tk.Label(
            self.status_bar_frame,
            text="⚠ Mô phỏng",
            font=(self.font_family, 10, "bold"),
            padx=10,
            pady=2,
            relief=tk.SOLID,
            borderwidth=1,
        )
        self.mock_badge.pack(side=tk.RIGHT)

    # -------------------------------------------------------------------------
    # Theme & Styling
    # -------------------------------------------------------------------------

    def _apply_theme(self) -> None:
        """Apply the active color theme to all UI elements."""
        th = self.theme

        # Root and Main container
        self.root.configure(bg=th["bg_root"])
        self.main_container.configure(bg=th["bg_root"])
        self.header_frame.configure(bg=th["bg_card"])
        self._branding_frame.configure(bg=th["bg_card"])
        self._display_frame.configure(bg=th["bg_card"])

        # Header elements
        self.title_label.configure(bg=th["bg_card"], fg=th["fg_text"])
        self.subtitle_header_label.configure(bg=th["bg_card"], fg=th["fg_subtext"])
        self.font_label.configure(bg=th["bg_card"], fg=th["fg_text"])
        self.font_value_label.configure(bg=th["bg_card"], fg=th["fg_text"])

        # Font buttons
        for btn in (self.font_minus_btn, self.font_plus_btn):
            btn.configure(
                bg=th["btn_bg"],
                fg=th["btn_fg"],
                activebackground=th["btn_active"],
                activeforeground=th["btn_fg"],
            )

        # Font slider
        self.font_slider.configure(
            bg=th["bg_card"],
            fg=th["fg_text"],
            troughcolor=th["control_bg"],
            activebackground=th["btn_active"],
        )

        # Contrast button
        contrast_text = "☀️ Chế độ sáng" if self.dark_mode else "🌙 Chế độ tối"
        self.contrast_btn.configure(
            text=contrast_text,
            bg=th["btn_bg"],
            fg=th["btn_fg"],
            activebackground=th["btn_active"],
            activeforeground=th["btn_fg"],
        )

        # Control Toolbar
        self.control_frame.configure(bg=th["bg_root"])
        self._action_frame.configure(bg=th["bg_root"])

        # Mode frame & radios
        self.mode_group.configure(
            bg=th["bg_card"],
            fg=th["fg_text"],
            bd=1,
            highlightbackground=th["border"],
        )
        self.radio_mode_asr.configure(
            bg=th["bg_card"],
            fg=th["fg_text"],
            selectcolor=th["control_bg"],
            activebackground=th["bg_card"],
            activeforeground=th["fg_text"],
        )
        self.radio_mode_exp.configure(
            bg=th["bg_card"],
            fg=th["fg_text"],
            selectcolor=th["control_bg"],
            activebackground=th["bg_card"],
            activeforeground=th["fg_text"],
        )

        # Source frame & radios
        self.source_group.configure(
            bg=th["bg_card"],
            fg=th["fg_text"],
            bd=1,
            highlightbackground=th["border"],
        )
        for r_btn in (self.radio_source_a, self.radio_source_v, self.radio_source_av):
            r_btn.configure(
                bg=th["bg_card"],
                fg=th["fg_text"],
                selectcolor=th["control_bg"],
                activebackground=th["bg_card"],
                activeforeground=th["fg_text"],
            )

        # Start/Stop Button
        self._update_start_stop_button()

        # Status Indicator Badge
        self._update_status_indicator_style(self.current_status)

        # Subtitle Area
        self.subtitle_outer_frame.configure(bg=th["bg_root"])
        self.subtitle_box.configure(
            bg=th["bg_subtitle"],
            highlightbackground=th["border"],
        )
        self.subtitle_label.configure(
            bg=th["bg_subtitle"],
            fg=th["fg_subtitle"],
        )
        self.subtitle_meta_label.configure(
            bg=th["bg_subtitle"],
            fg=th["fg_subtext"],
        )

        # Status Bar
        self.status_bar_frame.configure(
            bg=th["status_bar_bg"],
            highlightbackground=th["border"],
        )
        self.status_mode_label.configure(
            bg=th["status_bar_bg"],
            fg=th["fg_text"],
        )
        self.status_device_label.configure(
            bg=th["status_bar_bg"],
            fg=th["fg_subtext"],
        )

        # Mock Badge
        if self.mock_mode:
            self.mock_badge.configure(
                text="⚠ Mô phỏng",
                bg=th["mock_badge_bg"],
                fg=th["mock_badge_fg"],
            )
        else:
            # "Thu trực tiếp" is honest: live devices are open, but no
            # recogniser is connected yet (no TV4 pipeline).
            self.mock_badge.configure(
                text="● Thu trực tiếp",
                bg=th["real_badge_bg"],
                fg=th["real_badge_fg"],
            )

    def _update_status_indicator_style(self, status: str) -> None:
        """Update the status indicator label with proper background and foreground colors.

        Args:
            status: One of the STATUS_* constants.
        """
        self.current_status = status
        theme_key = "dark" if self.dark_mode else "light"
        colors = STATUS_COLORS.get(status, STATUS_COLORS[STATUS_READY])[theme_key]
        self.status_indicator.configure(
            text=status,
            bg=colors[0],
            fg=colors[1],
        )

    def _update_start_stop_button(self) -> None:
        """Update Start/Stop button appearance according to execution state."""
        th = self.theme
        if self.is_running:
            self.start_stop_btn.configure(
                text="Dừng",
                bg=th["stop_btn_bg"],
                fg="#ffffff",
                activebackground="#991b1b",
                activeforeground="#ffffff",
            )
        else:
            self.start_stop_btn.configure(
                text="Bắt đầu",
                bg=th["start_btn_bg"],
                fg="#ffffff",
                activebackground="#15803d",
                activeforeground="#ffffff",
            )

    # -------------------------------------------------------------------------
    # Event Handlers & User Interactions
    # -------------------------------------------------------------------------

    def _on_start_stop(self) -> None:
        """Toggle recognition start/stop state."""
        if not self.is_running:
            # Start recording / recognition turn
            self.is_running = True
            self._stop_event.clear()
            self._recording_done_event.clear()

            # Update UI state
            self._update_start_stop_button()
            self._update_status_indicator_style(STATUS_RECORDING)

            # Lock mode switching during execution
            self.radio_mode_asr.configure(state=tk.DISABLED)
            self.radio_mode_exp.configure(state=tk.DISABLED)
            self.radio_source_a.configure(state=tk.DISABLED)
            self.radio_source_v.configure(state=tk.DISABLED)
            self.radio_source_av.configure(state=tk.DISABLED)

            # Snapshot mode & source on main thread for thread-safe access by workers
            self._active_mode = self.mode_var.get()
            self._active_source = self.source_var.get()

            # Launch worker thread
            if self.mock_mode:
                self._worker_thread = threading.Thread(
                    target=self._process_mock,
                    args=(self._active_mode, self._active_source),
                    daemon=True,
                    name="AuralensMockWorker",
                )
                self._worker_thread.start()
            else:
                # Placeholder for live capture & inference integration
                self._worker_thread = threading.Thread(
                    target=self._process_live,
                    daemon=True,
                    name="AuralensLiveWorker",
                )
                self._worker_thread.start()
        else:
            # User clicked "Dừng" while active
            if self.current_status == STATUS_RECORDING:
                # Advance from recording directly to processing
                self._recording_done_event.set()
                self._update_status_indicator_style(STATUS_PROCESSING)
            else:
                # Request immediate abort
                self._stop_event.set()
                self._recording_done_event.set()

    def _on_mode_change(self) -> None:
        """Handle mode switcher changes between ASR free and 10-sentence experiment."""
        selected_mode = self.mode_var.get()
        if selected_mode == MODE_EXPERIMENT_10:
            # Show Source selector
            self.source_group.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
            src = self.source_var.get()
            self.status_mode_label.configure(
                text=f"Chế độ: {MODE_EXPERIMENT_10} [{src}]"
            )
        else:
            # Hide Source selector
            self.source_group.pack_forget()
            self.status_mode_label.configure(text=f"Chế độ: {MODE_ASR_FREE}")

    def _on_source_change(self) -> None:
        """Handle source selection change in experiment mode (A / V / AV)."""
        if self.mode_var.get() == MODE_EXPERIMENT_10:
            src = self.source_var.get()
            self.status_mode_label.configure(
                text=f"Chế độ: {MODE_EXPERIMENT_10} [{src}]"
            )

    def _toggle_contrast(self) -> None:
        """Toggle between high-contrast dark mode and light mode."""
        self.dark_mode = not self.dark_mode
        self._apply_theme()

    def _adjust_font_size(self, delta: int) -> None:
        """Adjust subtitle font size by delta (bounded between 16 and 48).

        Args:
            delta: Increment or decrement step in points.
        """
        new_size = max(16, min(48, self.font_size + delta))
        self._set_font_size(new_size)

    def _on_slider_change(self, val: str) -> None:
        """Handle font slider motion."""
        try:
            self._set_font_size(int(val))
        except (ValueError, TypeError):
            pass

    def _set_font_size(self, new_size: int) -> None:
        """Set subtitle font size and update UI elements."""
        self.font_size = max(16, min(48, int(new_size)))
        if self.font_size_var.get() != self.font_size:
            self.font_size_var.set(self.font_size)
        self.font_value_label.configure(text=f"{self.font_size} pt")
        self.subtitle_label.configure(
            font=(self.font_family, self.font_size, "bold")
        )

    def _on_subtitle_box_resize(self, event: tk.Event) -> None:
        """Dynamically adjust subtitle label wraplength when container resizes."""
        # Subtract padding to ensure words never clip
        new_wrap = max(200, event.width - 48)
        self.subtitle_label.configure(wraplength=new_wrap)

    # -------------------------------------------------------------------------
    # Worker Thread & Queue Polling
    # -------------------------------------------------------------------------

    def _process_mock(
        self,
        mode: Optional[str] = None,
        source: Optional[str] = None,
    ) -> None:
        """Simulate audio-visual speech recognition workflow with realistic delay.

        Args:
            mode: Operational mode string passed from main thread.
            source: Selected source ('A', 'V', 'AV') passed from main thread.
        """
        try:
            # Resolve mode and source safely without touching Tkinter variables
            active_mode = mode if mode is not None else getattr(self, "_active_mode", MODE_ASR_FREE)
            active_source = source if source is not None else getattr(self, "_active_source", SOURCE_AV)

            # Phase 1: Recording simulation (up to 1.8 seconds or until user presses Stop)
            self.queue.put({"type": "status", "status": STATUS_RECORDING})

            # Check for user clicking "Dừng" or app close every 50ms
            waited = 0.0
            max_rec_wait = 1.8
            while waited < max_rec_wait:
                if self._stop_event.is_set() or self._is_closing:
                    return
                if self._recording_done_event.is_set():
                    break
                time.sleep(0.05)
                waited += 0.05

            if self._stop_event.is_set() or self._is_closing:
                return

            # Phase 2: Processing simulation (0.8 - 1.2 seconds delay)
            self.queue.put({"type": "status", "status": STATUS_PROCESSING})

            processing_delay = random.uniform(0.7, 1.1)
            time.sleep(processing_delay)

            if self._stop_event.is_set() or self._is_closing:
                return

            # Phase 3: Result Generation based on active Mode & Source

            if active_mode == MODE_ASR_FREE:
                # Free Vietnamese ASR sentence
                result_text = random.choice(MOCK_ASR_SENTENCES)
                result_status = STATUS_READY
                meta_text = "Nguồn: Âm thanh ASR (Tự do) | infer: 840ms"
            else:
                # 10-Sentence Experiment mode
                # Simulate recognition confidence based on source:
                # AV: highest accuracy, A: moderate, V (visual-only): highest chance of uncertainty
                uncertain_chance = {
                    SOURCE_AV: 0.05,
                    SOURCE_AUDIO: 0.15,
                    SOURCE_VISUAL: 0.30,
                }.get(active_source, 0.10)

                source_labels = {
                    SOURCE_AV: "Nghe–Nhìn (AV)",
                    SOURCE_AUDIO: "Âm thanh (A)",
                    SOURCE_VISUAL: "Hình ảnh / Khẩu hình (V)",
                }

                if random.random() < uncertain_chance:
                    result_text = UNCERTAIN_EXPERIMENT_TEXT
                    result_status = STATUS_UNCERTAIN
                    meta_text = f"Nguồn: {source_labels[active_source]} | Độ tin cậy thấp"
                else:
                    result_text = random.choice(PREDEFINED_10_SENTENCES)
                    result_status = STATUS_READY
                    meta_text = f"Nguồn: {source_labels[active_source]} | Phân loại 10 câu | infer: 620ms"

            # Post result to queue for main thread to update UI
            self.queue.put({
                "type": "subtitle",
                "text": result_text,
                "status": result_status,
                "meta": meta_text,
                "finished": True,
            })

        except Exception as ex:
            logger.exception("Error during mock processing: %s", ex)
            self.queue.put({
                "type": "error",
                "text": f"Lỗi hệ thống: {str(ex)}",
                "status": STATUS_ERROR,
                "finished": True,
            })

    def _process_live(self) -> None:
        """Live turn: open the real devices, record one turn, then release them.

        Runs on a worker thread. The recorder is opened at the start of the turn
        and closed in ``finally`` — on success, on error and on window close —
        which is what guarantees the camera/microphone are not left held.

        No recogniser exists yet (the TV4 pipeline has not been handed over), so
        the turn ends with an ``uncertain`` subtitle carrying real capture
        numbers. It never invents a recognised sentence.
        """
        recorder = None
        try:
            self.queue.put({"type": "status", "status": STATUS_RECORDING})

            recorder = self._recorder_factory(
                camera_index=self.camera_index,
                audio_device=self.audio_device,
                sample_rate=self.sample_rate,
                max_duration_s=self.max_duration_s,
            )
            self._recorder = recorder
            recorder.open()

            # Label comes from what the device actually reports, not a fixed string.
            self.queue.put(
                {
                    "type": "device",
                    "text": self._format_device_label(recorder.device_info),
                }
            )

            sample_id = f"tv5-{int(time.time() * 1000)}"
            recorder.start_recording(sample_id)

            # Wait for "Dừng", the window closing, or an automatic stop because a
            # capture limit (duration / frame cap) was reached.
            while not self._recording_done_event.wait(0.05):
                if self._stop_event.is_set() or self._is_closing:
                    break
                if not recorder.is_recording or getattr(
                    recorder, "limit_reached", False
                ):
                    break

            captured = recorder.stop_recording()

            # User aborted the turn: drop it instead of showing a stale result.
            if self._stop_event.is_set() or self._is_closing:
                return

            audio = captured["audio"]
            frames = captured["video_frames"]
            sample_id = captured["sample_id"]

            # Report the length of what was actually buffered: when the duration
            # cap stops capture, the session is longer than the content.
            sample_rate = int(captured["sample_rate"]) or 1
            seconds = (
                len(audio) / sample_rate
                if len(audio)
                else captured["duration_ms"] / 1000.0
            )

            # Persist the turn as pilot data. Saving happens on this worker
            # thread and must not hide the capture numbers if the disk write
            # fails, so the error is reported instead of raised.
            saved: Optional[Dict[str, Any]] = None
            save_error = ""
            try:
                from auralens.capture.storage import save_capture

                saved = save_capture(captured, self.output_dir)
            except Exception as ex:
                logger.exception("Failed to save capture %s", sample_id)
                save_error = str(ex)

            limit_note = ""
            if captured.get("limit_reached"):
                reason = captured.get("limit_reason") or "thời lượng"
                limit_note = f" · dừng ở giới hạn {reason}"

            if saved is None:
                text = f"Đã thu {seconds:.1f} giây — chưa lưu được file"
                file_note = f"lỗi lưu: {save_error}" if save_error else "chưa lưu file"
            else:
                text = f"Đã thu {seconds:.1f} giây — đã lưu mẫu {sample_id}"
                file_note = f"lưu tại {saved['directory']}"

            self.queue.put(
                {
                    "type": "subtitle",
                    "text": text + limit_note,
                    "status": STATUS_UNCERTAIN,
                    "meta": (
                        f"{sample_id} · {len(audio)} mẫu @ "
                        f"{captured['sample_rate']} Hz · {len(frames)} frame · "
                        f"{file_note} · chưa nối TV4"
                    ),
                    "finished": True,
                }
            )
        except Exception as ex:
            logger.exception("Live capture failed: %s", ex)
            self.queue.put(
                {
                    "type": "error",
                    "text": f"Lỗi thiết bị: {ex}",
                    "status": STATUS_ERROR,
                    "finished": True,
                }
            )
        finally:
            if recorder is not None:
                try:
                    recorder.close()
                except Exception:
                    logger.exception("Failed to close Recorder")
                if self._recorder is recorder:
                    self._recorder = None
                self.queue.put(
                    {"type": "device", "text": "Thiết bị: đã nhả camera & micro"}
                )

    def _poll_queue(self) -> None:
        """Poll the message queue from background workers and update UI on main thread."""
        if self._is_closing:
            return

        try:
            while True:
                message = self.queue.get_nowait()
                msg_type = message.get("type")

                if msg_type == "status":
                    status = message.get("status", STATUS_READY)
                    self._update_status_indicator_style(status)

                elif msg_type == "subtitle":
                    text = message.get("text", "")
                    status = message.get("status", STATUS_READY)
                    meta = message.get("meta", "")
                    self._update_subtitle(text, status)
                    if meta:
                        self.subtitle_meta_label.configure(text=meta)

                    if message.get("finished", False):
                        self._finish_run()

                elif msg_type == "device":
                    self._update_device_label(message.get("text", ""))

                elif msg_type == "error":
                    text = message.get("text", "Lỗi")
                    self._update_subtitle(text, STATUS_ERROR)
                    self.subtitle_meta_label.configure(text="Đã phát sinh lỗi trong quá trình xử lý")
                    if message.get("finished", False):
                        self._finish_run()

                self.queue.task_done()
        except queue.Empty:
            pass

        # Schedule next poll
        if not self._is_closing:
            self.root.after(100, self._poll_queue)

    @staticmethod
    def _format_device_label(info: Dict[str, Any]) -> str:
        """Build the status-bar device text from Recorder.device_info."""
        width = int(info.get("camera_width") or 0)
        height = int(info.get("camera_height") or 0)
        mic = str(info.get("mic_device_name") or "không rõ")
        if len(mic) > 30:
            mic = mic[:29] + "…"
        if width and height:
            return f"Thiết bị: camera {width}×{height} · mic {mic}"
        return f"Thiết bị: camera đã mở · mic {mic}"

    def _update_device_label(self, text: str) -> None:
        """Apply a device status message produced by the worker thread."""
        if text:
            self.status_device_label.configure(text=text)

    def _update_subtitle(self, text: str, status: str = STATUS_READY) -> None:
        """Update the subtitle display and status indicator from the main thread.

        Args:
            text: Subtitle text string to display.
            status: Status string (STATUS_READY, STATUS_UNCERTAIN, STATUS_ERROR, etc.).
        """
        self.subtitle_label.configure(text=text)
        self._update_status_indicator_style(status)

    def _finish_run(self) -> None:
        """Reset run state and unlock UI controls when processing completes."""
        self.is_running = False
        self._update_start_stop_button()

        # Re-enable mode and source selectors
        self.radio_mode_asr.configure(state=tk.NORMAL)
        self.radio_mode_exp.configure(state=tk.NORMAL)
        self.radio_source_a.configure(state=tk.NORMAL)
        self.radio_source_v.configure(state=tk.NORMAL)
        self.radio_source_av.configure(state=tk.NORMAL)

    # -------------------------------------------------------------------------
    # Lifecycle & Cleanup
    # -------------------------------------------------------------------------

    def _on_close(self) -> None:
        """Properly handle window close event, ensuring all worker threads terminate."""
        if self._is_closing:
            return
        self._is_closing = True

        # Signal background thread to stop
        self._stop_event.set()
        self._recording_done_event.set()

        # Wait briefly for worker thread to exit cleanly
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=0.4)

        # The worker closes its recorder in finally; if it is still stuck in a
        # driver call, close here too so devices are never left held open.
        recorder = self._recorder
        self._recorder = None
        if recorder is not None:
            try:
                recorder.close()
            except Exception:
                logger.exception("Failed to release capture devices on close")

        # Destroy window
        try:
            self.root.destroy()
        except Exception:
            pass

    def run(self) -> None:
        """Start the Tkinter event loop."""
        self.root.mainloop()


def main() -> None:
    """Entry point for running the Auralens Tkinter application directly."""
    root = tk.Tk()
    app = AuralensApp(root=root, mock_mode=True)
    app.run()


if __name__ == "__main__":
    main()
