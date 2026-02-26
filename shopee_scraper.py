import asyncio
import json
import logging
import urllib.parse
import pandas as pd
import os
import time
from typing import List, Dict, Any, Optional
from playwright.async_api import async_playwright
from playwright_stealth.stealth import Stealth

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ShopeeFlexibleScraper:
    def __init__(self, keyword: str):
        self.base_url = "https://shopee.vn"
        self.profile_dir = os.path.abspath("./shopee_profile")
        self.all_products = []
        self.unique_item_ids = set()
        self.keyword = keyword
        # Tên file đi theo từ khóa để bạn dễ quản lý
        clean_keyword = "".join([c if c.isalnum() else "_" for c in keyword])
        self.filename = f"shopee_{clean_keyword}_{int(time.time())}.csv"

    def save_data(self):
        """Lưu dữ liệu vào file CSV"""
        if self.all_products:
            try:
                df = pd.DataFrame(self.all_products)
                df.to_csv(self.filename, index=False, encoding='utf-8-sig')
                logger.info(f"--- Đã cập nhật {len(self.all_products)} sản phẩm vào {self.filename} ---")
            except PermissionError:
                logger.error(f"KHÔNG THỂ LƯU: Hãy đóng file {self.filename} nếu đang mở bằng Excel!")
            except Exception as e:
                logger.error(f"Lỗi khi lưu file: {e}")

    async def auto_scroll(self, page):
        """Macro cuộn trang thông minh"""
        logger.info(f"Đang cuộn trang để tải dữ liệu...")
        for i in range(12):
            await page.evaluate(f"window.scrollBy(0, {700})")
            await asyncio.sleep(0.8)
        await asyncio.sleep(2)

    async def run(self, max_pages: int = 5):
        async with async_playwright() as p:
            logger.info(f"Đang khởi động trình duyệt để cào: '{self.keyword}'")
            
            context = await p.chromium.launch_persistent_context(
                user_data_dir=self.profile_dir,
                headless=False,
                channel="chrome",
                no_viewport=True,
                ignore_default_args=["--enable-automation", "--no-sandbox"],
                args=["--start-maximized"]
            )
            
            page = context.pages[0]
            await Stealth().apply_stealth_async(page)

            # Lắng nghe dữ liệu Network
            async def handle_response(response):
                if "search/search_items" in response.url:
                    try:
                        data = await response.json()
                        items = data.get('items') or data.get('data', {}).get('items')
                        if items:
                            for item_wrapper in items:
                                item = item_wrapper.get('item_basic') or item_wrapper
                                if not item or not item.get('itemid'): continue
                                
                                item_id = item.get('itemid')
                                if item_id not in self.unique_item_ids:
                                    self.unique_item_ids.add(item_id)
                                    self.all_products.append({
                                        "name": item.get('name'),
                                        "price": item.get('price') / 100000 if item.get('price') else 0,
                                        "sold": item.get('historical_sold') or item.get('sold'),
                                        "rating": item.get('item_rating', {}).get('rating_star'),
                                        "location": item.get('shop_location'),
                                        "url": f"https://shopee.vn/product/{item.get('shopid')}/{item_id}",
                                        "scraped_keyword": self.keyword
                                    })
                    except:
                        pass

            page.on("response", handle_response)

            # Điều hướng thẳng tới trang tìm kiếm của từ khóa đó
            search_url = f"{self.base_url}/search?keyword={urllib.parse.quote(self.keyword)}"
            await page.goto(search_url)
            
            logger.info("------------------------------------------------------------")
            logger.info(f"MỤC TIÊU: {self.keyword}")
            logger.info("1. Đăng nhập và giải Captcha trên trình duyệt (nếu có).")
            logger.info("2. Khi đã thấy danh sách sản phẩm hiện ra, quay lại đây nhấn ENTER.")
            logger.info("------------------------------------------------------------")
            
            await asyncio.get_event_loop().run_in_executor(None, input, "==> Nhấn ENTER để BẮT ĐẦU CÀO TỰ ĐỘNG...")

            for p_idx in range(max_pages):
                logger.info(f"\n>>> ĐANG XỬ LÝ TRANG {p_idx + 1}/{max_pages}...")
                
                # Luôn đảm bảo đang ở đúng URL trang đó
                newest = p_idx * 60
                target_url = f"{self.base_url}/search?keyword={urllib.parse.quote(self.keyword)}&newest={newest}&page={p_idx}"
                
                if page.url != target_url:
                    await page.goto(target_url, wait_until="domcontentloaded")
                    await asyncio.sleep(2)

                await self.auto_scroll(page)
                self.save_data()
                
                await asyncio.sleep(2)

            logger.info(f"\nHOÀN TẤT! Tổng cộng thu thập: {len(self.all_products)} sản phẩm.")
            logger.info(f"Kết quả lưu tại: {os.path.abspath(self.filename)}")
            await context.close()

if __name__ == "__main__":
    print("=== CHƯƠNG TRÌNH CÀO DỮ LIỆU SHOPEE V2 ===")
    user_keyword = input("Nhập từ khóa bạn muốn cào (VD: kem, quần áo nam...): ")
    user_pages = input("Nhập số lượng trang muốn cào (mỗi trang ~60 SP, mặc định 5): ")
    
    if not user_pages.isdigit():
        user_pages = 5
    else:
        user_pages = int(user_pages)
        
    scraper = ShopeeFlexibleScraper(user_keyword)
    asyncio.run(scraper.run(max_pages=user_pages))
