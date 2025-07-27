import base64
import bz2
import zlib
import marshal
import dis
import os

# Tên tệp chứa mã bị làm rối
file_to_decode = 'CTOOL.py'

# Kiểm tra xem tệp có tồn tại không
if not os.path.exists(file_to_decode):
    print(f"Lỗi: Không tìm thấy tệp '{file_to_decode}'. Vui lòng đảm bảo tệp này tồn tại trong kho chứa.")
    exit(1)

# Đọc nội dung đã bị làm rối từ tệp
with open(file_to_decode, 'rb') as f:
    obfuscated_content = f.read()

# Tìm và trích xuất chuỗi mã hóa base85
try:
    # Trích xuất phần dữ liệu base85 một cách an toàn
    start_marker = b"base64.a85decode(b'"
    end_marker = b"')))"
    start_index = obfuscated_content.find(start_marker) + len(start_marker)
    end_index = obfuscated_content.rfind(end_marker)
    encoded_string = obfuscated_content[start_index:end_index]

    # 1. Giải mã Base85
    compressed_data_zlib = base64.a85decode(encoded_string)

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
