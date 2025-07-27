import base64
import bz2
import zlib
import marshal
import dis
import os
import re

# Tên tệp bạn muốn giải mã
FILENAME = 'CTOOL.py.txt' 

try:
    print(f"--- Bắt đầu giải mã tệp: {FILENAME} ---")

    # Đọc tệp dưới dạng bytes
    with open(FILENAME, 'rb') as f:
        content = f.read()
    print(f"✅ Đã đọc thành công {len(content)} bytes từ tệp.")

    # Dùng Regex để tìm và trích xuất chuỗi mã hóa
    match = re.search(rb"a85decode\(b'([^']*)'\)", content)
    if not match:
        raise ValueError("Không tìm thấy chuỗi mã hóa. Hãy đảm bảo tệp đầu vào là phiên bản gốc.")

    encoded_string = match.group(1)
    print("✅ Đã trích xuất chuỗi mã hóa.")

    # Thực hiện các bước giải mã theo đúng thứ tự
    print("1. Đang giải mã Base85...")
    data = base64.a85decode(encoded_string)
    print("2. Đang giải nén BZ2...")
    data = bz2.decompress(data)
    print("3. Đang giải nén ZLIB...")
    data = zlib.decompress(data)
    print("4. Đang tải dữ liệu Marshal...")
    code_obj = marshal.loads(data)

    # In kết quả cuối cùng
    print("\n" + "="*50)
    print("--- ✅ GIẢI MÃ THÀNH CÔNG ---")
    print("--- Mã Bytecode của chương trình: ---")
    dis.dis(code_obj)
    print("="*50)

except Exception as e:
    print(f"\n--- ❌ LỖI TRONG QUÁ TRÌNH GIẢI MÃ ---")
    print(f"Lỗi: {e}")
    exit(1) # Thoát với mã lỗi để GitHub Actions báo cáo thất bại