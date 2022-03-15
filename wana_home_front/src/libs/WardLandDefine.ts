export interface House {
    'server': number,
    'territory_id': number,
    'ward_id': number,
    'house_id': number,
    'price': number,
    'owner': string,
}

export interface HouseSimple {
    price: number
    owner: string
}

export const territories: { [k: number]: { full: string, short: string } } = {
    339: {full: "海雾村", short: "海"},
    341: {full: "高脚孤丘", short: "沙"},
    340: {full: "薰衣草苗园", short: "森"},
    641: {full: "白银乡", short: "白"},
    979: {full: "雪景房", short: "雪"},
}
export const ward_cnt = 24
export const house_cnt = 60

export const dc_server = [
    {
        "dc_name": "陆行鸟",
        "servers": {
            1042: "拉诺西亚",
            1044: "幻影群岛",
            1060: "萌芽池",
            1081: "神意之地",
            1167: "红玉海",
            1173: "宇宙和音",
            1174: "沃仙曦染",
            1175: "晨曦王座"
        }
    },
    {
        "dc_name": "莫古力",
        "servers": {
            1076: "白金幻象",
            1113: "旅人栈桥",
            1121: "拂晓之间",
            1166: "龙巢神殿",
            1170: "潮风亭",
            1171: "神拳痕",
            1172: "白银乡",
            1176: "梦羽宝境"
        }
    },
    {
        "dc_name": "猫小胖",
        "servers": {
            1043: "紫水栈桥",
            1045: "摩杜纳",
            1106: "静语庄园",
            1169: "延夏",
            1177: "海猫茶屋",
            1178: "柔风海湾",
            1179: "琥珀原"
        }
    },
    {
        "dc_name": "豆豆柴",
        "servers": {
            1183: "银泪湖",
            1192: "水晶塔",
            1180: "太阳海岸",
            1186: "伊修加德",
            1193: "红茶川"
        }
    },
]

export const servers: { [key: number]: string } = {
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
}

export function house_size(size_id: number) {
    switch (size_id) {
        case 1:
            return 'S';
        case 2:
            return 'M';
        case 3:
            return 'L';
        default:
            return size_id;
    }
}
