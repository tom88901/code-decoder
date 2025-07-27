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

# Đọc toàn bộ nội dung tệp dưới dạng bytes
with open(file_to_decode, 'rb') as f:
    obfuscated_content = f.read()

try:
    # --- BIỂU THỨC CHÍNH QUY CHÍNH XÁC ---
    # Tìm kiếm chuỗi nằm bên trong a85decode(b'...'). Đây là phương pháp đáng tin cậy nhất.
    match = re.search(rb"a85decode\(b'([^']*)'\)", obfuscated_content)
    
    if not match:
        raise ValueError("Không thể tìm thấy chuỗi mã hóa trong hàm a85decode.")
        
    encoded_string = match.group(1)
    
    # Các bước giải mã đảo ngược đúng thứ tự
    # 1. Giải mã Base85
    data_after_b85 = base64.a85decode(encoded_string)

    # 2. Giải nén BZ2
    data_after_bz2 = bz2.decompress(data_after_b85)

    # 3. Giải nén ZLIB
    marshaled_code = zlib.decompress(data_after_bz2)

    # 4. Tải đối tượng mã bằng marshal
    code_obj = marshal.loads(marshaled_code)

    # 5. Phân tách và in mã bytecode
    print(f"--- BẮT ĐẦU GIẢI MÃ BYTECODE TỪ TỆP: {file_to_decode} ---")
    dis.dis(code_obj)
    print("--- KẾT THÚC GIẢI MÃ ---")
    print("\n✅ GIẢI MÃ THÀNH CÔNG! HÃY KIỂM TRA KẾT QUẢ Ở TRÊN.")

except Exception as e:
    print(f"❌ Đã xảy ra lỗi trong quá trình giải mã: {e}")