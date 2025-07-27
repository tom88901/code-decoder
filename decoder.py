import base64
import bz2
import zlib
import marshal
import dis
import os
import re

# Tên tệp chứa mã bị làm rối
file_to_decode = 'CTOOL.py'

if not os.path.exists(file_to_decode):
    print(f"Lỗi: Không tìm thấy tệp '{file_to_decode}'.")
    exit(1)

with open(file_to_decode, 'rb') as f:
    obfuscated_content = f.read()

try:
    # Sử dụng Regular Expression để tìm chuỗi mã hóa
    match = re.search(rb"a85decode\(b'([^']*)'\)", obfuscated_content)
    
    if not match:
        raise ValueError("Không thể tìm thấy chuỗi mã hóa base85 hợp lệ.")
        
    encoded_string = match.group(1)
    
    # 1. Giải mã Base85
    # Xử lý các ký tự escape ('\\') trước khi giải mã
    encoded_string_fixed = encoded_string.decode('unicode_escape').encode('latin1')
    data_after_b85 = base64.a85decode(encoded_string_fixed)

    # --- PHẦN SỬA LỖI QUAN TRỌNG ---
    # Đảo ngược đúng thứ tự: bz2 -> zlib
    
    # 2. Giải nén bz2
    data_after_bz2 = bz2.decompress(data_after_b85)

    # 3. Giải nén zlib
    marshaled_code = zlib.decompress(data_after_bz2)
    # --- KẾT THÚC PHẦN SỬA LỖI ---

    # 4. Tải đối tượng mã bằng marshal
    code_obj = marshal.loads(marshaled_code)

    # 5. Phân tách và in mã bytecode một cách an toàn
    print(f"--- Bắt đầu giải mã bytecode từ tệp: {file_to_decode} ---")
    dis.dis(code_obj)
    print("--- Kết thúc giải mã ---")
    print("\n✅ Giải mã thành công! Xem kết quả ở trên.")

except Exception as e:
    print(f"❌ Đã xảy ra lỗi trong quá trình giải mã: {e}")