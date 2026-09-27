# Chạy một bộ kiểm với trình duyệt đặt ở 9 giờ sáng hôm nay, giờ Việt Nam.
# Bọc hàm mở trang của công cụ thử — không sửa mã bộ kiểm.
import runpy, sys, datetime
from playwright.sync_api._generated import Browser
VN=datetime.timezone(datetime.timedelta(hours=7))
now=datetime.datetime.now(VN); MORNING=now.replace(hour=9,minute=0,second=0,microsecond=0)
def new_page(self, *a, **k):
    k.setdefault('timezone_id','Asia/Ho_Chi_Minh')
    pg=self.new_context(**k).new_page()
    pg.clock.install(time=MORNING)
    return pg
Browser.new_page=new_page
sys.argv=[sys.argv[1]]
runpy.run_path(sys.argv[0], run_name='__main__')
