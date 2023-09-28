#!/usr/bin/env python3
import webbrowser

from ttkbootstrap import LabelFrame, Button, Entry, Label

from .right_clicker import RightClicker
from ..gui_windows.signal_get_auth_window import SignalGetAuthWindow
from ..gui_windows.line_get_auth_window import LineGetAuthWindow
from ..gui_windows.kakao_get_auth_window import KakaoGetAuthWindow

class CredFrame:
    def __init__(self, gui):
        self.gui = gui
        self.frame = LabelFrame(self.gui.scrollable_frame, borderwidth=1, text='Credentials')

        self.frame.grid_columnconfigure(1, weight=1)

        self.signal_uuid_lbl = Label(self.frame, text='Signal uuid', width=18, justify='left', anchor='w')
        self.signal_uuid_entry = Entry(self.frame, textvariable=self.gui.signal_uuid_var, width=50, validate="focusout", validatecommand=self.gui.highlight_fields)
        self.signal_uuid_entry.bind('<Button-3><ButtonRelease-3>', RightClicker)

        self.signal_password_lbl = Label(self.frame, text='Signal password', justify='left', anchor='w')
        self.signal_password_entry = Entry(self.frame, textvariable=self.gui.signal_password_var, width=50, validate="focusout", validatecommand=self.gui.highlight_fields)
        self.signal_password_entry.bind('<Button-3><ButtonRelease-3>', RightClicker)

        self.signal_get_auth_btn = Button(self.frame, text='Generate', command=self.cb_signal_get_auth, bootstyle='secondary')

        self.telegram_token_lbl = Label(self.frame, text='Telegram token', justify='left', anchor='w')
        self.telegram_token_entry = Entry(self.frame, textvariable=self.gui.telegram_token_var, width=50, validate="focusout", validatecommand=self.gui.highlight_fields)
        self.telegram_token_entry.bind('<Button-3><ButtonRelease-3>', RightClicker)

        self.telegram_userid_lbl = Label(self.frame, text='Telegram user_id', justify='left', anchor='w')
        self.telegram_userid_entry = Entry(self.frame, textvariable=self.gui.telegram_userid_var, width=50, validate="focusout", validatecommand=self.gui.highlight_fields)
        self.telegram_userid_entry.bind('<Button-3><ButtonRelease-3>', RightClicker)

        self.kakao_auth_token_lbl = Label(self.frame, text='Kakao auth_token', justify='left', anchor='w')
        self.kakao_auth_token_entry = Entry(self.frame, textvariable=self.gui.kakao_auth_token_var, width=35)
        self.kakao_auth_token_entry.bind('<Button-3><ButtonRelease-3>', RightClicker)
        self.kakao_get_auth_btn = Button(self.frame, text='Generate', command=self.cb_kakao_get_auth, bootstyle='secondary')

        self.line_cookies_lbl = Label(self.frame, text='Line cookies', width=18, justify='left', anchor='w')
        self.line_cookies_entry = Entry(self.frame, textvariable=self.gui.line_cookies_var, width=35)
        self.line_cookies_entry.bind('<Button-3><ButtonRelease-3>', RightClicker)
        self.line_get_auth_btn = Button(self.frame, text='Generate', command=self.cb_line_get_auth, bootstyle='secondary')

        self.help_btn = Button(self.frame, text='Get help', command=self.cb_cred_help, bootstyle='secondary')

        self.signal_uuid_lbl.grid(column=0, row=0, sticky='w', padx=3, pady=3)
        self.signal_uuid_entry.grid(column=1, row=0, columnspan=2, sticky='w', padx=3, pady=3)
        self.signal_password_lbl.grid(column=0, row=1, sticky='w', padx=3, pady=3)
        self.signal_password_entry.grid(column=1, row=1, columnspan=2, sticky='w', padx=3, pady=3)
        self.signal_get_auth_btn.grid(column=2, row=2, sticky='e', padx=3, pady=3)
        self.telegram_token_lbl.grid(column=0, row=3, sticky='w', padx=3, pady=3)
        self.telegram_token_entry.grid(column=1, row=3, columnspan=2, sticky='w', padx=3, pady=3)
        self.telegram_userid_lbl.grid(column=0, row=4, sticky='w', padx=3, pady=3)
        self.telegram_userid_entry.grid(column=1, row=4, columnspan=2, sticky='w', padx=3, pady=3)
        self.kakao_auth_token_lbl.grid(column=0, row=5, sticky='w', padx=3, pady=3)
        self.kakao_auth_token_entry.grid(column=1, row=5, sticky='w', padx=3, pady=3)
        self.kakao_get_auth_btn.grid(column=2, row=5, sticky='e', padx=3, pady=3)
        self.line_cookies_lbl.grid(column=0, row=6, sticky='w', padx=3, pady=3)
        self.line_cookies_entry.grid(column=1, row=6, sticky='w', padx=3, pady=3)
        self.line_get_auth_btn.grid(column=2, row=6, sticky='e', padx=3, pady=3)
        self.help_btn.grid(column=2, row=8, sticky='e', padx=3, pady=3)
    
    def cb_cred_help(self, *args):
        faq_site = 'https://github.com/laggykiller/sticker-convert#faq'
        success = webbrowser.open(faq_site)
        if not success:
            self.gui.cb_ask_str('You can get help from:', initialvalue=faq_site)
    
    def cb_kakao_get_auth(self, *args):
        KakaoGetAuthWindow(self.gui)
    
    def cb_signal_get_auth(self, *args):
        SignalGetAuthWindow(self.gui)
    
    def cb_line_get_auth(self, *args):
        LineGetAuthWindow(self.gui)
    
    def set_states(self, state):
        self.signal_uuid_entry.config(state=state)
        self.signal_password_entry.config(state=state)
        self.signal_get_auth_btn.config(state=state)
        self.telegram_token_entry.config(state=state)
        self.telegram_userid_entry.config(state=state)
        self.kakao_auth_token_entry.config(state=state)
        self.kakao_get_auth_btn.config(state=state)
        self.line_cookies_entry.config(state=state)
        self.line_get_auth_btn.config(state=state)
