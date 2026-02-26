# Project Price Scrap Ver 2

Dự án cào dữ liệu sản phẩm và giá cả từ Shopee sử dụng Python và Playwright.

## Tính năng
- Trích xuất thông tin sản phẩm: tên, giá, đánh giá, metadata...
- Xử lý nội dung động và JavaScript bằng Playwright.
- Sử dụng plugin stealth để hạn chế bị phát hiện là bot.
- Xuất dữ liệu ra file CSV thuận tiện cho việc xử lý bằng Pandas hoặc Excel.

## Công nghệ sử dụng
- **Python**: Ngôn ngữ lập trình chính.
- **Playwright**: Thư viện tự động hóa trình duyệt.
- **playwright-stealth**: Plugin ẩn danh cho Playwright.
- **Pandas**: Xử lý và xuất dữ liệu.

## Cài đặt

### Yêu cầu hệ thống
- Python 3.8+
- pip (Trình quản lý gói Python)

### Các bước cài đặt
1. Tạo môi trường ảo (khuyến nghị):
   ```bash
   python -m venv venv
   # Trên Windows:
   venv\Scripts\activate
   # Trên Linux/Mac:
   source venv/bin/activate
   ```

2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

3. Cài đặt trình duyệt cho Playwright:
   ```bash
   playwright install chromium
   ```

## Cách sử dụng
Để chạy script cào dữ liệu:
```bash
python shopee_scraper.py
```
Sau khi chạy, chương trình sẽ yêu cầu bạn nhập:
- **Từ khóa**: Tên sản phẩm bạn muốn tìm kiếm.
- **Số trang**: Số lượng trang kết quả bạn muốn cào (mỗi trang chứa khoảng 60 sản phẩm).

Dữ liệu sẽ được lưu tự động vào file CSV trong thư mục gốc với tên file định dạng: `shopee_[từ_khóa]_[timestamp].csv`.

## Kiểm thử
Chạy các bài kiểm tra bằng pytest:
```bash
pytest
```

## Lưu ý
Dự án sử dụng thư mục `shopee_profile` để lưu trữ dữ liệu trình duyệt, giúp duy trì trạng thái đăng nhập hoặc cấu hình trình duyệt nếu cần.
