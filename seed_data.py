from sqlmodel import Session, select
from database import engine
from models import Product, Review


def seed_db():
    with Session(engine) as session:
        # 检查是否已经有数据
        existing = session.exec(select(Product)).first()
        if existing:
            print("数据库已经有数据了，跳过插入。")
            print("如果你非要重新插入，请先在左侧删除 shopping.db 文件，然后重启服务，再运行本脚本。")
            return

        # 1. 准备 20 个假商品数据
        products = [
            # --- 笔记本 ---
            Product(name="联想拯救者 Y9000P", category="笔记本", price=8999.0, stock=50,
                    description="i9-13900HX, RTX4060显卡, 16G内存, 1T固态, 2.5K电竞屏", rating=4.8),
            Product(name="MacBook Air M2", category="笔记本", price=7999.0, stock=30,
                    description="8核CPU, 10核GPU, 8G内存, 256G固态, 13.6英寸Liquid视网膜屏", rating=4.9),
            Product(name="华硕天选4 锐龙版", category="笔记本", price=7299.0, stock=80,
                    description="R7-7735H, RTX4060, 16G内存, 512G固态, 15.6英寸144Hz电竞屏", rating=4.6),
            Product(name="戴尔 XPS 13", category="笔记本", price=12999.0, stock=10,
                    description="i7处理器, 16G内存, 512G固态, 13.4英寸全面屏, 极致轻薄商务本", rating=4.5),
            Product(name="惠普暗影精灵9", category="笔记本", price=8499.0, stock=0,
                    description="i9-13900HX, RTX4060, 16G, 1T, 240Hz高刷电竞屏 (目前缺货)", rating=4.7),

            # --- 手机 ---
            Product(name="iPhone 15 Pro", category="手机", price=7999.0, stock=100,
                    description="A17 Pro芯片, 钛金属边框, 8G内存, 128G存储, 4800万像素主摄", rating=4.7),
            Product(name="iPhone 15", category="手机", price=5999.0, stock=150,
                    description="A16芯片, 灵动岛设计, 6G内存, 128G存储, 4800万像素主摄", rating=4.8),
            Product(name="华为 Mate 60 Pro", category="手机", price=6999.0, stock=20,
                    description="麒麟9000s, 卫星通话, 12G内存, 512G存储, 鸿蒙系统", rating=4.9),
            Product(name="小米 14", category="手机", price=3999.0, stock=200,
                    description="骁龙8Gen3, 徕卡光学镜头, 12G内存, 256G存储, 澎湃OS", rating=4.8),
            Product(name="红米 K70", category="手机", price=2499.0, stock=500,
                    description="骁龙8Gen2, 2K直屏, 12G内存, 256G存储, 极致性价比", rating=4.6),
            Product(name="一加 12", category="手机", price=4299.0, stock=60,
                    description="骁龙8Gen3, 哈苏影像, 16G内存, 512G存储, 2K东方屏", rating=4.7),
            Product(name="vivo X100", category="手机", price=3999.0, stock=80,
                    description="天玑9300, 蔡司影像, 12G内存, 256G存储", rating=4.7),

            # --- 耳机 ---
            Product(name="索尼 WH-1000XM5", category="耳机", price=2299.0, stock=200,
                    description="头戴式, 顶级主动降噪, 30小时续航, 佩戴舒适", rating=4.9),
            Product(name="Apple AirPods Pro 2", category="耳机", price=1899.0, stock=300,
                    description="入耳式, 降噪升级, H2芯片, 支持空间音频", rating=4.8),
            Product(name="Bose QC45", category="耳机", price=1999.0, stock=50,
                    description="头戴式, 经典降噪, 24小时续航, 适合差旅", rating=4.6),
            Product(name="漫步者花再", category="耳机", price=399.0, stock=500,
                    description="半入耳式, 高颜值, 蓝牙5.3, 长续航, 学生党首选", rating=4.5),

            # --- 外设 ---
            Product(name="罗技 GPW 二代", category="鼠标", price=699.0, stock=150,
                    description="轻量化无线电竞鼠标, 63g, HERO 25K传感器", rating=4.8),
            Product(name="雷蛇 毒蝰 V2 Pro", category="鼠标", price=899.0, stock=0,
                    description="超轻量无线鼠标, 58g, Focus Pro 30K传感器", rating=4.7),
            Product(name="腹灵 F12 机械键盘", category="键盘", price=299.0, stock=120,
                    description="68键, 三模无线, 热插拔, RGB背光", rating=4.6),
            Product(name="罗技 MX Master 3S", category="鼠标", price=599.0, stock=80,
                    description="办公神器, 人体工学设计, 静音按键, 8K DPI", rating=4.9),
        ]

        session.add_all(products)
        session.commit()

        for p in products:
            session.refresh(p)
        print(f"成功插入 {len(products)} 个商品！")

        # 2. 准备假评论数据（挑几个热门商品写）
        reviews = [
            # 联想拯救者
            Review(product_id=products[0].id, user_name="张同学", rating=5.0,
                   content="性能怪兽，打赛博朋克完全不卡，散热也很好！"),
            Review(product_id=products[0].id, user_name="李老板", rating=4.0,
                   content="机器很重，加上砖头一样的电源，适合放宿舍，不适合天天背去图书馆。"),
            # MacBook Air
            Review(product_id=products[1].id, user_name="王女士", rating=5.0,
                   content="非常轻薄，续航简直无敌，一天不充电完全没问题。适合写代码和办公。"),
            # 华为
            Review(product_id=products[7].id, user_name="赵总", rating=5.0,
                   content="遥遥领先！信号非常好，电梯里也能刷视频，卫星通话很酷。"),
            # 小米14
            Review(product_id=products[8].id, user_name="极客刘", rating=5.0,
                   content="首发买的，系统很流畅，徕卡拍照很出片，小屏手感真棒。"),
            Review(product_id=products[8].id, user_name="路人甲", rating=3.0, content="打游戏稍微有点发热，其他都挺好。"),
            # 索尼耳机
            Review(product_id=products[12].id, user_name="考研党", rating=5.0,
                   content="降噪无敌，戴上之后全世界都安静了，图书馆必备。"),
            # 漫步者耳机
            Review(product_id=products[15].id, user_name="女大学生", rating=4.0,
                   content="颜值超级高，音质对于这个价格来说很能打了。"),
            # 罗技GPW
            Review(product_id=products[16].id, user_name="电竞少年", rating=5.0,
                   content="打FPS神器，非常轻，用久了手腕不累。"),
        ]

        session.add_all(reviews)
        session.commit()
        print(f"成功插入 {len(reviews)} 条评论！")


if __name__ == "__main__":
    seed_db()