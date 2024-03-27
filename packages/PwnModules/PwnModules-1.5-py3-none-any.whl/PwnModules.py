"""
@author: RedLeaves
@date: 2023-4-24
Pwntools-Extern Functions
开源包，任何人都可以使用并修改！
"""

from LibcSearcher import *
from pwn import *
import re

__version__ = '1.5'

def leak_addr(i, io_i):
	"""
	获取泄露的内存地址。

	Args:
		i (int): 用于指定地址获取方式的参数。可以是0、1或2。0是32位，1是64位正向接收，2是64位反向接收。
		io_i: IO流。

	Returns:
		int: 返回获取到的内存地址。
	"""
	if i == 0:
		address_internal = u32(io_i.recv(4))
		return address_internal
	if i == 1:
		address_internal = u64(io_i.recvuntil(b'\x7f')[:6].ljust(8, b'\x00'))
		return address_internal
	if i == 2:
		address_internal = u64(io_i.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))
		return address_internal

def libc_remastered(func, addr_i, onlineMode=False):
	"""
	在没有提供Libc版本时，这个参数可以快捷的使用LibcSearcher获取常用函数地址。

	Args:
		func: 泄露的函数
		addr_i: 泄露的函数的地址
		onlineMode: 在线搜索还是在本地Libc库搜索

	Returns:
		int: libc_base, system, /bin/sh 的地址。
	"""
	libc_i = LibcSearcher(func, addr_i, online=onlineMode)
	libc_base_i = addr_i - libc_i.dump(func)
	sys_i = libc_base_i + libc_i.dump('system')
	sh_i = libc_base_i + libc_i.dump('str_bin_sh')
	return libc_base_i, sys_i, sh_i

def debug(io):
	"""
	快捷GDB Attach函数。

	Args:
		io: IO流
	"""
	gdb.attach(io)
	pause()

def recv_int_addr(io, num):
	"""
	获取泄露的Int地址，一般是格式化字符串泄露Canary等。

	Args:
		io: IO流
		num: 需要接收几位数字

	Returns:
		int: Int地址的十进制格式。
	"""
	return int(io.recv(num), 16)

def show_addr(msg, *args, **kwargs):
	"""
	打印地址。

	Args:
		msg: 在打印地址前显示的文本
		*args: 需要打印的内存地址
		**kwargs: 需要打印的内存地址
	"""
	msg = f'\x1b[01;38;5;90m{msg}\x1b[0m'
	colored_text = '\x1b[01;38;5;90m' + ': ' + '\x1b[0m'

	for arg in args:
		hex_text = hex(arg)
		colored_hex_text = f'\x1b[01;38;5;90m{hex_text}\x1b[0m'
		print(f"{msg}{colored_text}{colored_hex_text}")

	for key, value in kwargs.items():
		hex_text = hex(value)
		colored_hex_text = f'\x1b[01;38;5;90m{hex_text}\x1b[0m'
		print(f"{msg}{colored_text}{key}{colored_hex_text}")

def init_env(arch, loglevel='info'):
	"""
	初始化环境，默认为 amd64 架构，info 级日志打印。

	Args:
		arch: 系统架构
		log_level: 日志打印等级
	"""
	if (arch == 'amd64'):
		context(arch='amd64', os='linux', log_level=loglevel)
	else:
		context(arch='x86', os='linux', log_level=loglevel)

def get_utils(binary, local=True, ip=None, port=None):
	"""
	快速获取IO流和ELF。

	Args:
		binary: 二进制文件
		local: 布尔值，本地模式或在线
		ip: 在线IP
		port: 在线Port

	Returns:
		io: IO流
		elf: ELF引用
	"""
	elf = ELF(binary)

	if not local:
		io = remote(ip, port)
		return io, elf

	else:
		io = process(binary)
		return io, elf

def fmtstraux(io=None, size=None, x64=True):
	"""
	快速获取格式化字符串对应的偏移。
	
	Args:
		io: IO流
		size: 几个%p，默认为10
		x64: 是否是64位
		
	Returns:
		int: 格式化字符串偏移
	"""
	if size is None:
		size = 10

	if x64 is True:
		strsize = 8
	else:
		strsize = 4

	Payload = b'A' * strsize + b'-%p' * size

	io.sendline(Payload)
	
	temp = io.recvline()

	pattern = re.compile(r'(0x[0-9a-fA-F]+|\(nil\))(?:-|$)')

	matches = pattern.findall(temp.decode())

	if matches:
		position = 0
		for match in matches:
			if match == b'(nil)':
				position += 1
			else:
				position += 1
				if x64 is True:
					if match == '0x4141414141414141':
						return position
						break
				else:
					if match == '0x41414141':
						return position
						break

	else:
		print("Unknown Error.")
			
