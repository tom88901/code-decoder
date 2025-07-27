import base64
import bz2
import zlib
import marshal
import dis
import os
import re

file_to_decode = 'CTOOL.py'

if not os.path.exists(file_to_decode):
    print(f"Lỗi: Không tìm thấy tệp '{file_to_decode}'.")
    exit(1)

with open(file_to_decode, 'rb') as f:
    obfuscated_content = f.read()

try:
    # --- SỬA LỖI BIỂU THỨC CHÍNH QUY ---
    # Pattern này tìm kiếm chuỗi nằm giữa `_pymeomeo=b'` và `'` cuối cùng
    # Nó đơn giản và phù hợp chính xác với cấu trúc tệp của bạn.
    match = re.search(rb"_pymeomeo=b'([^']*)'", obfuscated_content)
    
    if not match:
        raise ValueError("Không thể tìm thấy chuỗi mã hóa base85 hợp lệ.")
        
    encoded_string = match.group(1)
    # --- KẾT THÚC SỬA LỖI ---
    
    # 1. Giải mã Base85
    data_after_b85 = base64.a85decode(encoded_string)

    # 2. Giải nén BZ2
    data_after_bz2 = bz2.decompress(data_after_b85)

    # 3. Giải nén ZLIB
    marshaled_code = zlib.decompress(data_after_bz2)

    # 4. Tải đối tượng mã bằng marshal
    code_obj = marshal.loads(marshaled_code)

    # 5. Phân tách và in mã bytecode
    print(f"--- Bắt đầu giải mã bytecode từ tệp: {file_to_decode} ---")
    dis.dis(code_obj)
    print("--- Kết thúc giải mã ---")
    print("\n✅ Giải mã thành công! Xem kết quả ở trên.")

except Exception as e:
    print(f"❌ Đã xảy ra lỗi trong quá trình giải mã: {e}")