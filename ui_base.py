import tkinter as tk
from abc import ABC, abstractmethod
from config import AppConfig


class BaseWindow(ABC):
    
    def __init__(self):
        self.config = AppConfig()
        self.window = None
    
    @abstractmethod
    def setup_ui(self):
        pass
    
    def get_color(self, color_key):
        return self.config.colors.get(color_key, 'white')
    
    def run(self):
        if self.window:
            self.window.mainloop()
    
    def close(self):
        if self.window:
            self.window.destroy()


class BaseFrame(ABC):
    
    def __init__(self, parent):
        self.parent = parent
        self.config = AppConfig()
        self.frame = None
    
    @abstractmethod
    def create(self):
        pass
    
    def get_color(self, color_key):
        return self.config.colors.get(color_key, 'white')
