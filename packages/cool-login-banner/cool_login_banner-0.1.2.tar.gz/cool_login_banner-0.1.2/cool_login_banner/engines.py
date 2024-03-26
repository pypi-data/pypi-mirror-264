import cowsay
import pyfiglet
import termcolor
from abc import ABC, abstractmethod
from typing import Iterable
from colorama import Fore, Back, Style, just_fix_windows_console

just_fix_windows_console()

STYLE_LST = {
    'blink': '\x1b[5m',
    'bold': '\x1b[1m',
    'underline': '\x1b[4m',
    'reverse': '\x1b[7m',
    'strikethrough': '\x1b[9m',
}


class Engine(ABC):

    @abstractmethod
    def generate_original_banner(self, *args, **kwargs):
        pass

    def generate_banner(self, *args: str, fore_color: str = None, back_color: str = None,
                        styles: Iterable[str] = None, preview: bool = True, **kwargs: str) -> str:
        """生成banner"""

        banner = self.generate_original_banner(*args, **kwargs)
        if fore_color is not None:
            banner = getattr(Fore, fore_color.upper()) + banner
        if back_color is not None:
            banner = getattr(Back, back_color.upper()) + banner
        if styles is not None:
            banner = ''.join([STYLE_LST[s] for s in styles if s in STYLE_LST] + [banner])
        banner = banner + Style.RESET_ALL
        if preview:
            print(banner)
        return banner

    @property
    def fore_colors(self) -> list[str]:
        """返回前景色列表"""

        return list(Fore.__dict__.keys())

    @property
    def back_colors(self) -> list[str]:
        """返回背景色列表"""

        return list(Back.__dict__.keys())

    @property
    def styles(self) -> list[str]:
        """返回样式列表"""

        return list(STYLE_LST.keys())

    @staticmethod
    def preview_fore_colors() -> None:
        """前景色预览"""

        for color in Fore.__dict__:
            print(getattr(Fore, color.upper()) + color)

        print(Style.RESET_ALL)

    @staticmethod
    def preview_back_colors() -> None:
        """背景色预览"""

        for color in Back.__dict__:
            print(getattr(Back, color.upper()) + color)

        print(Style.RESET_ALL)

    @staticmethod
    def preview_styles() -> None:
        """样式预览"""

        for name, code in STYLE_LST.items():
            print(f'{code}{name}{termcolor.RESET}')


class TextEngine(Engine):
    """纯文本引擎"""
    def generate_original_banner(self, text: str) -> str:
        """只是原样返回文本"""

        return text


class FigletEngine(Engine):
    def generate_original_banner(self, text: str, font: str = pyfiglet.DEFAULT_FONT, **kwargs: str) -> str:
        """返回pyfiglet生成的图案"""

        return pyfiglet.figlet_format(text, font, **kwargs)

    @property
    def figlet_fonts(self) -> list[str]:
        """返回pyfiglet的字体样式列表"""

        return pyfiglet.FigletFont.getFonts()


class CowsayEngine(Engine):
    def generate_original_banner(self, text: str, pattern: str = 'cow') -> str:
        """返回cowsay图案，如果传入的pattern不属于内置的图案，则直接使用这个pattern生成图案"""

        if pattern in self.patterns:
            return cowsay.get_output_string(pattern, text) + '\n'
        else:
            return cowsay.draw(text, pattern, False)

    @property
    def patterns(self) -> list[str]:
        """返回cowsay内置的图案列表"""

        return cowsay.char_names

    def preview_patterns(self) -> None:
        """预览所有图案"""

        for pattern in self.patterns:
            getattr(cowsay, pattern)(text=pattern)
