import configparser
from utils import rand_char
from pathlib import Path

current = Path()

config = configparser.ConfigParser()
config.read(current / 'sample.config.ini', encoding='utf-8')

config['django']['key'] = rand_char(32)

new_config = configparser.ConfigParser()
new_config.add_section('upload')
new_config['upload']['url'] = ''

servers = ["拉诺西亚", "幻影群岛", "萌芽池", "神意之地", "红玉海", "宇宙和音", "沃仙曦染", "晨曦王座",
           "白金幻象", "旅人栈桥", "拂晓之间", "龙巢神殿", "潮风亭", "神拳痕", "白银乡", "梦羽宝境",
           "紫水栈桥", "摩杜纳", "静语庄园", "延夏", "海猫茶屋", "柔风海湾", "琥珀原",
           "水晶塔","银泪湖","太阳海岸","伊修加德","红茶川"]
for server in servers:
    config['tokens'][server] = rand_char(32)
    new_config['upload'][server] = config['tokens'][server]

fp = current / 'config.ini'
with open(current / 'gen.config.ini' if fp.exists() else fp, 'w+', encoding='utf-8') as f:
    config.write(f)
print('generate config file at:', fp)

fp = current / 'upload.ini'
with open(current / 'gen.upload.ini' if fp.exists() else fp, 'w+', encoding='utf-8') as f:
    new_config.write(f)
print('generate upload config at:', fp)
