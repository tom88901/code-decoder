import base64
import bz2
import zlib
import marshal
import dis
import os

file_to_decode = 'CTOOL.py'

if not os.path.exists(file_to_decode):
    print(f"Lỗi: Không tìm thấy tệp '{file_to_decode}'.")
    exit(1)

with open(file_to_decode, 'rb') as f:
    obfuscated_content = f.read()

try:
    # --- PHƯƠNG PHÁP TRÍCH XUẤT MỚI, ĐƠN GIẢN VÀ HIỆU QUẢ ---
    # 1. Tìm điểm bắt đầu của chuỗi mã hóa
    start_marker = b"_pymeomeo=b'"
    start_index = obfuscated_content.find(start_marker)
    
    if start_index == -1:
        raise ValueError("Không tìm thấy điểm bắt đầu của chuỗi mã hóa (_pymeomeo=b').")
    
    # Dữ liệu bắt đầu ngay sau marker
    start_index += len(start_marker)

    # 2. Tìm điểm kết thúc của chuỗi mã hóa (dấu ' ngay sau đó)
    end_index = obfuscated_content.find(b"'", start_index)

    if end_index == -1:
        raise ValueError("Không tìm thấy điểm kết thúc của chuỗi mã hóa.")

    # 3. Cắt chuỗi mã hóa ra
    encoded_string = obfuscated_content[start_index:end_index]
    # --- KẾT THÚC PHƯƠNG PHÁP MỚI ---

    # Các bước giải mã giữ nguyên như cũ
    data_after_b85 = base64.a85decode(encoded_string)
    data_after_bz2 = bz2.decompress(data_after_b85)
    marshaled_code = zlib.decompress(data_after_bz2)
    code_obj = marshal.loads(marshaled_code)

    # In kết quả
    print(f"--- Bắt đầu giải mã bytecode từ tệp: {file_to_decode} ---")
    dis.dis(code_obj)
    print("--- Kết thúc giải mã ---")
    print("\n✅ Giải mã thành công! Xem kết quả ở trên.")

except Exception as e:
    print(f"❌ Đã xảy ra lỗi trong quá trình giải mã: {e}")