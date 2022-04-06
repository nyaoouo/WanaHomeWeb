from functools import cache

from utils.Config import config

servers = {
    1042: "拉诺西亚",
    1044: "幻影群岛",
    1060: "萌芽池",
    1081: "神意之地",
    1167: "红玉海",
    1173: "宇宙和音",
    1174: "沃仙曦染",
    1175: "晨曦王座",
    1076: "白金幻象",
    1113: "旅人栈桥",
    1121: "拂晓之间",
    1166: "龙巢神殿",
    1170: "潮风亭",
    1171: "神拳痕",
    1172: "白银乡",
    1176: "梦羽宝境",
    1043: "紫水栈桥",
    1045: "摩杜纳",
    1106: "静语庄园",
    1169: "延夏",
    1177: "海猫茶屋",
    1178: "柔风海湾",
    1179: "琥珀原",
    1183: "银泪湖",
    1192: "水晶塔",
    1180: "太阳海岸",
    1186: "伊修加德",
    1193: "红茶川",
}


@cache
def get_server_token(server_id):
    if server_id not in servers:
        return None
    try:
        return config['tokens'][servers[server_id]]
    except KeyError:
        return None
