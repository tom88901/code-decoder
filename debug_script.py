import re
import os

FILENAME = 'CTOOL.py'
print(f"--- BẮT ĐẦU DEBUG: KIỂM TRA TỆP '{FILENAME}' ---")

# 1. Kiểm tra sự tồn tại của tệp
if not os.path.exists(FILENAME):
    print(f"❌ LỖI NGHIÊM TRỌNG: Không tìm thấy tệp '{FILENAME}' trong thư mục làm việc.")
    exit(1)

print("✅ Tệp tồn tại.")

# 2. Đọc nội dung tệp dưới dạng bytes
with open(FILENAME, 'rb') as f:
    content_bytes = f.read()

print(f"✅ Đã đọc thành công {len(content_bytes)} bytes từ tệp.")

# 3. Thử tìm chuỗi mã hóa bằng Biểu thức chính quy (Phương pháp 1)
print("\n--- Thử Phương pháp 1: Biểu thức chính quy ---")
match = re.search(rb"a85decode\(b'([^']*)'\)", content_bytes)

if match:
    extracted_string = match.group(1)
    print("✅ SUCCESS: Đã tìm thấy chuỗi mã hóa!")
    print(f"   - Độ dài chuỗi: {len(extracted_string)} bytes")
    print(f"   - 50 ký tự đầu: {extracted_string[:50]}")
    print(f"   - 50 ký tự cuối: {extracted_string[-50:]}")
else:
    print("❌ FAILED: Không tìm thấy chuỗi mã hóa bằng biểu thức chính quy.")
    # Nếu thất bại, in ra một phần nội dung để xem tại sao
    print("\n--- Nội dung tệp (200 bytes đầu) để kiểm tra ---")
    print(content_bytes[:200])
    print("-------------------------------------------------")