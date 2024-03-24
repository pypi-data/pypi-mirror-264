#!/usr/bin/env python3
from typing import TYPE_CHECKING, Any

from ttkbootstrap import Button, Checkbutton, Entry, Label, LabelFrame, OptionMenu  # type: ignore

from sticker_convert.gui_components.frames.right_clicker import RightClicker
from sticker_convert.gui_components.windows.advanced_compression_window import AdvancedCompressionWindow

if TYPE_CHECKING:
    from sticker_convert.gui import GUI  # type: ignore


class CompFrame(LabelFrame):
    def __init__(self, gui: "GUI", *args: Any, **kwargs: Any) -> None:
        self.gui = gui
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(2, weight=1)

        self.no_compress_help_btn = Button(
            self,
            text="?",
            width=1,
            command=lambda: self.gui.cb_msg_block(self.gui.help["comp"]["no_compress"]),
            bootstyle="secondary",  # type: ignore
        )
        self.no_compress_lbl = Label(self, text="No compression")
        self.no_compress_cbox = Checkbutton(
            self,
            variable=self.gui.no_compress_var,
            command=self.cb_no_compress,
            onvalue=True,
            offvalue=False,
            bootstyle="danger-round-toggle",  # type: ignore
        )

        self.comp_preset_help_btn = Button(
            self,
            text="?",
            width=1,
            command=lambda: self.gui.cb_msg_block(self.gui.help["comp"]["preset"]),
            bootstyle="secondary",  # type: ignore
        )
        self.comp_preset_lbl = Label(self, text="Preset")
        self.comp_preset_opt = OptionMenu(
            self,
            self.gui.comp_preset_var,
            self.gui.comp_preset_var.get(),
            *self.gui.compression_presets.keys(),
            command=self.cb_comp_apply_preset,
            bootstyle="secondary",  # type: ignore
        )
        self.comp_preset_opt.config(width=15)

        self.steps_help_btn = Button(
            self,
            text="?",
            width=1,
            command=lambda: self.gui.cb_msg_block(self.gui.help["comp"]["steps"]),
            bootstyle="secondary",  # type: ignore
        )
        self.steps_lbl = Label(self, text="Number of steps")
        self.steps_entry = Entry(self, textvariable=self.gui.steps_var, width=8)
        self.steps_entry.bind("<Button-3><ButtonRelease-3>", RightClicker)

        self.processes_help_btn = Button(
            self,
            text="?",
            width=1,
            command=lambda: self.gui.cb_msg_block(self.gui.help["comp"]["processes"]),
            bootstyle="secondary",  # type: ignore
        )
        self.processes_lbl = Label(self, text="Number of processes")
        self.processes_entry = Entry(self, textvariable=self.gui.processes_var, width=8)
        self.processes_entry.bind("<Button-3><ButtonRelease-3>", RightClicker)

        self.comp_advanced_btn = Button(
            self,
            text="Advanced...",
            command=self.cb_compress_advanced,
            bootstyle="secondary",  # type: ignore
        )

        self.no_compress_help_btn.grid(column=0, row=0, sticky="w", padx=3, pady=3)
        self.no_compress_lbl.grid(column=1, row=0, sticky="w", padx=3, pady=3)
        self.no_compress_cbox.grid(column=2, row=0, sticky="nes", padx=3, pady=3)

        self.comp_preset_help_btn.grid(column=0, row=1, sticky="w", padx=3, pady=3)
        self.comp_preset_lbl.grid(column=1, row=1, sticky="w", padx=3, pady=3)
        self.comp_preset_opt.grid(column=2, row=1, sticky="nes", padx=3, pady=3)

        self.steps_help_btn.grid(column=0, row=2, sticky="w", padx=3, pady=3)
        self.steps_lbl.grid(column=1, row=2, sticky="w", padx=3, pady=3)
        self.steps_entry.grid(column=2, row=2, sticky="nes", padx=3, pady=3)

        self.processes_help_btn.grid(column=0, row=3, sticky="w", padx=3, pady=3)
        self.processes_lbl.grid(column=1, row=3, sticky="w", padx=3, pady=3)
        self.processes_entry.grid(column=2, row=3, sticky="nes", padx=3, pady=3)

        self.comp_advanced_btn.grid(column=2, row=4, sticky="nes", padx=3, pady=3)

        self.cb_comp_apply_preset()
        self.cb_no_compress()

    def cb_comp_apply_preset(self, *_: Any) -> None:
        selection = self.gui.get_preset()
        if selection == "auto":
            if self.gui.get_input_name() == "local":
                self.gui.no_compress_var.set(True)
            else:
                self.gui.no_compress_var.set(False)

        self.gui.fps_min_var.set(self.gui.compression_presets[selection]["fps"]["min"])
        self.gui.fps_max_var.set(self.gui.compression_presets[selection]["fps"]["max"])
        self.gui.fps_power_var.set(
            self.gui.compression_presets[selection]["fps"]["power"]
        )
        self.gui.res_w_min_var.set(
            self.gui.compression_presets[selection]["res"]["w"]["min"]
        )
        self.gui.res_w_max_var.set(
            self.gui.compression_presets[selection]["res"]["w"]["max"]
        )
        self.gui.res_h_min_var.set(
            self.gui.compression_presets[selection]["res"]["h"]["min"]
        )
        self.gui.res_h_max_var.set(
            self.gui.compression_presets[selection]["res"]["h"]["max"]
        )
        self.gui.res_power_var.set(
            self.gui.compression_presets[selection]["res"]["power"]
        )
        self.gui.quality_min_var.set(
            self.gui.compression_presets[selection]["quality"]["min"]
        )
        self.gui.quality_max_var.set(
            self.gui.compression_presets[selection]["quality"]["max"]
        )
        self.gui.quality_power_var.set(
            self.gui.compression_presets[selection]["quality"]["power"]
        )
        self.gui.color_min_var.set(
            self.gui.compression_presets[selection]["color"]["min"]
        )
        self.gui.color_max_var.set(
            self.gui.compression_presets[selection]["color"]["max"]
        )
        self.gui.color_power_var.set(
            self.gui.compression_presets[selection]["color"]["power"]
        )
        self.gui.duration_min_var.set(
            self.gui.compression_presets[selection]["duration"]["min"]
        )
        self.gui.duration_max_var.set(
            self.gui.compression_presets[selection]["duration"]["max"]
        )
        self.gui.img_size_max_var.set(
            self.gui.compression_presets[selection]["size_max"]["img"]
        )
        self.gui.vid_size_max_var.set(
            self.gui.compression_presets[selection]["size_max"]["vid"]
        )
        self.gui.img_format_var.set(
            self.gui.compression_presets[selection]["format"]["img"]
        )
        self.gui.vid_format_var.set(
            self.gui.compression_presets[selection]["format"]["vid"]
        )
        self.gui.fake_vid_var.set(self.gui.compression_presets[selection]["fake_vid"])
        self.gui.scale_filter_var.set(
            self.gui.compression_presets[selection]["scale_filter"]
        )
        self.gui.quantize_method_var.set(
            self.gui.compression_presets[selection]["quantize_method"]
        )
        self.gui.default_emoji_var.set(
            self.gui.compression_presets[selection]["default_emoji"]
        )
        self.gui.steps_var.set(self.gui.compression_presets[selection]["steps"])

        self.cb_no_compress()
        self.gui.highlight_fields()

    def cb_compress_advanced(self, *_: Any) -> None:
        AdvancedCompressionWindow(self.gui)

    def cb_no_compress(self, *_: Any) -> None:
        if self.gui.no_compress_var.get() is True:
            state = "disabled"
        else:
            state = "normal"

        self.comp_advanced_btn.config(state=state)
        self.steps_entry.config(state=state)
        self.processes_entry.config(state=state)

    def set_inputs_comp(self, state: str) -> None:
        self.comp_preset_opt.config(state=state)
        self.comp_advanced_btn.config(state=state)
        self.steps_entry.config(state=state)
        self.processes_entry.config(state=state)

    def set_states(self, state: str) -> None:
        self.no_compress_cbox.config(state=state)
        self.set_inputs_comp(state=state)
