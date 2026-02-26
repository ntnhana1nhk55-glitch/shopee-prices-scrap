import pytest
import asyncio
from shopee_scraper import ShopeeFlexibleScraper

@pytest.mark.asyncio
async def test_scraper_init():
    # Test khởi tạo class
    scraper = ShopeeFlexibleScraper(keyword="kem chống nắng")
    assert scraper.keyword == "kem chống nắng"
    assert "shopee_profile" in scraper.profile_dir

@pytest.mark.asyncio
async def test_filename_generation():
    # Test xem tên file lưu có đúng định dạng không
    scraper = ShopeeFlexibleScraper(keyword="máy tính")
    assert scraper.filename.startswith("shopee_m_y_t_nh_")
    assert scraper.filename.endswith(".csv")

# Lưu ý: Không nên chạy test cào thật trong unit test để tránh bị Shopee block
# Chúng ta chỉ test các logic xử lý file và khởi tạo.
