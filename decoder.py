import base64
import bz2
import zlib
import marshal
import dis
import os
import re # Thêm thư viện re

# Tên tệp chứa mã bị làm rối
file_to_decode = 'CTOOL.py'

# Kiểm tra xem tệp có tồn tại không
if not os.path.exists(file_to_decode):
    print(f"Lỗi: Không tìm thấy tệp '{file_to_decode}'. Vui lòng đảm bảo tệp này tồn tại trong kho chứa.")
    exit(1)

# Đọc nội dung đã bị làm rối từ tệp
with open(file_to_decode, 'rb') as f:
    obfuscated_content = f.read()

try:
    # --- PHẦN ĐÃ SỬA LỖI (Nâng cấp) ---
    # Sử dụng Regular Expression để tìm chuỗi mã hóa một cách đáng tin cậy.
    # Pattern này sẽ tìm đoạn văn bản nằm bên trong b'...' của hàm a85decode.
    match = re.search(rb"a85decode\(b'([^']*)'\)", obfuscated_content)
    
    if not match:
        raise ValueError("Không thể tìm thấy chuỗi mã hóa base85 hợp lệ trong tệp.")
        
    encoded_string = match.group(1)
    # --- KẾT THÚC PHẦN SỬA LỖI ---

    # 1. Giải mã Base85
    # Lưu ý: Dữ liệu trong tệp gốc có một số ký tự '\' cần được un-escape
    # ví dụ \\ -> \. Python's decode('unicode_escape') sẽ xử lý việc này.
    encoded_string_fixed = encoded_string.decode('unicode_escape').encode('latin1')
    compressed_data_zlib = base64.a85decode(encoded_string_fixed)

    # 2. Giải nén zlib
    compressed_data_bz2 = zlib.decompress(compressed_data_zlib)

    # 3. Giải nén bz2
    marshaled_code = bz2.decompress(compressed_data_bz2)

    # 4. Tải đối tượng mã bằng marshal
    code_obj = marshal.loads(marshaled_code)

    # 5. Phân tách và in mã bytecode một cách an toàn
    print(f"--- Bắt đầu giải mã bytecode từ tệp: {file_to_decode} ---")
    dis.dis(code_obj)
    print("--- Kết thúc giải mã ---")
    print("\n✅ Giải mã thành công! Xem kết quả ở trên.")

except Exception as e:
    print(f"❌ Đã xảy ra lỗi trong quá trình giải mã: {e}")
    print("Vui lòng kiểm tra lại định dạng tệp hoặc chuỗi mã hóa.")