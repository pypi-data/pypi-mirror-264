from fabric import Connection
from invoke import sudo
from functools import partial
from io import BytesIO
from typing import ClassVar, Any
from .engines import Engine


class BannerSetter:
    SSHD_CONFIG_PATH: ClassVar[str] = '/etc/ssh/sshd_config'
    SSH_BANNER_PATH: ClassVar[str] = '/etc/ssh/login_banner'
    MOTD_PATH: ClassVar[str] = '/etc/motd'
    ISSUE_PATH: ClassVar[str] = '/etc/issue'
    ISSUE_NET_PATH: ClassVar[str] = '/etc/issue_net'

    def __init__(self, engine: type(Engine) | None = None, host: str | None = None, port: int = 22,
                 user: str | None = None, password: str | None = None, encoding: str = 'utf8', **kwargs):
        """用户需要有sudo权限，如果没有设置免密，还需提供password。所有关键字参数在内部都会传递给 ``fabric.Connection`` 构造函数"""

        self.engine = engine if engine is None else engine()

        if host:
            connect_kwargs = kwargs.setdefault('connect_kwargs', {})
            connect_kwargs['password'] = password
            self.conn = Connection(host, user=user, port=port, **kwargs)
            self.sudo = partial(self.conn.sudo, encoding=encoding, password=password, hide=True)
        else:
            self.sudo = partial(sudo, encoding=encoding, password=password, hide=True)

    def _save_text_to_file(self, text: str, file: str) -> None:
        """将字符串保存到文件中

        由于banner中包含各种字符，使用bash命令将内容保存到文件总是报非法字符错误，因此用了一个取巧的办法。
        直接保存为 BytesIO 文件，上传到服务器，然后再修改文件归属。
        """
        with BytesIO(text.encode('utf8')) as f:
            self.conn.put(f, '/tmp/tmp_banner')
            self.sudo(f'mv -f /tmp/tmp_banner {file}')
            self.sudo(f'chown root:root {file}')

    def _clear_file_content(self, file: str) -> None:
        """清空文件内容"""

        self.sudo(f'sed -i "/^/d" {file}')

    def save_ssh_banner(self, banner: str) -> None:
        """将banner保存到指定文件，配置/etc/ssh/sshd_config文件，并重启sshd服务"""

        self.clear_ssh_banner()
        self.sudo(f"sed -i '$a Banner {self.SSH_BANNER_PATH}' {self.SSHD_CONFIG_PATH}")
        self._save_text_to_file(banner, self.SSH_BANNER_PATH)
        self.sudo('systemctl restart sshd')

    def set_ssh_banner(self, *args: Any, **kwargs: Any) -> None:
        """生成ssh登录banner并进行相应配置，参数会直接送给引擎的 generate_banner 方法"""

        banner = self.generate_banner(*args, **kwargs)
        self.save_ssh_banner(banner)

    def clear_ssh_banner(self) -> None:
        """删除ssh登录banner文件，将/etc/ssh/sshd_config恢复默认值，并重启sshd服务"""

        self.sudo(f'rm -f {self.SSH_BANNER_PATH}')
        self.sudo(f'sed -i /^Banner/d {self.SSHD_CONFIG_PATH}')
        self.sudo('systemctl restart sshd')

    def save_motd_banner(self, banner: str) -> None:
        """将banner保存到/etc/motd文件"""

        self._save_text_to_file(banner, self.MOTD_PATH)

    def clear_motd_banner(self) -> None:
        """清空/etc/motd文件"""

        self._clear_file_content(self.MOTD_PATH)

    def set_motd_banner(self, *args: Any, **kwargs: Any) -> None:
        """生成banner并保存到/etc/motd文件，参数会送到引擎的generate_banner方法

        motd文件的内容，会在登录成功后显示

        """
        banner = self.generate_banner(*args, **kwargs)
        self.save_motd_banner(banner)

    def save_tty_banner(self, banner: str) -> None:
        """将banner保存到/etc/issue文件"""

        self._save_text_to_file(banner, self.ISSUE_PATH)

    def clear_tty_banner(self) -> None:
        """清空/etc/issue文件"""

        self._clear_file_content(self.ISSUE_PATH)

    def set_tty_banner(self, *args: Any, **kwargs: Any) -> None:
        """生成banner并保存到/etc/issue文件，参数会送到引擎的generate_banner方法

        issue文件的内容，会在本机使用tty登录之前显示，ssh远程登录应使用set_ssh_banner方法
        """

        banner = self.generate_banner(*args, **kwargs)
        self.save_tty_banner(banner)

    def save_telnet_banner(self, banner: str) -> None:
        """将banner保存到/etc/issue_net文件"""

        self._save_text_to_file(banner, self.ISSUE_NET_PATH)

    def clear_telnet_banner(self) -> None:
        """清空/etc/issue_net文件"""

        self._clear_file_content(self.ISSUE_NET_PATH)

    def set_telnet_banner(self, *args: Any, **kwargs: Any) -> None:
        """生成banner并保存到/etc/issue_net文件，参数会送到引擎的generate_banner方法

        issue_net文件的内容，会在使用telnet登录之前显示，ssh远程登录应使用set_ssh_banner方法
        """

        banner = self.generate_banner(*args, **kwargs)
        self.save_telnet_banner(banner)

    def __getattr__(self, name: str) -> Any:
        """其它方法和属性转接到engine实例"""

        if self.engine is None:
            raise ValueError("You haven't provided a banner engine yet")

        return getattr(self.engine, name)
