# IDAPython 在线文档 https://www.hex-rays.com/products/ida/support/idapython_docs/

import idaapi

def xor_bytes(start_addr, end_addr, key):
  for addr in range(start_addr, end_addr + 1):
    byte = idaapi.get_byte(addr)
    idaapi.patch_byte(addr, byte ^ key)

def main():
  start_addr = int(0x00403020)
  end_addr = int(0x00403083)
  key = int(0x67)
  xor_bytes(start_addr, end_addr, key)

if __name__ == "__main__":
  main()
