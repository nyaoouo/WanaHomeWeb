export const zero_pad = (num: number, places: number) => String(num).padStart(places, '0')

export function is_same_day(date1: Date, date2: Date) {
    return date1.getDate() === date2.getDate() &&
        date1.getMonth() === date2.getMonth() &&
        date1.getFullYear() === date2.getFullYear()
}

export function string_format(str: string, args: { [k: string]: any }) {
    for (var key in args)
        str = str.replace(new RegExp("\\{" + key + "\\}", "gi"), args[key].toString());
    return str;
}

export function date_format(date: Date, format_string: string) {
    return string_format(format_string, {
        Y: date.getFullYear().toString().substr(2),
        M: zero_pad(date.getMonth() + 1, 2),
        D: zero_pad(date.getDate(), 2),
        H: zero_pad(date.getHours(), 2),
        I: zero_pad(date.getMinutes(), 2),
        S: zero_pad(date.getSeconds(), 2),
    })
}

export function time_diff_sec(diff_sec: number, eng = true) {
    var rtn = ''
    if (diff_sec >= 3600) {
        rtn += `${Math.round(diff_sec / 3600)}${eng ? 'h' : '小时'}`;
        diff_sec %= 3600;
    }
    if (diff_sec >= 60) {
        rtn += `${Math.round(diff_sec / 60)}${eng ? 'm' : '分钟'}`;
        diff_sec %= 60;
    }
    rtn += `${diff_sec}${eng ? 's' : '秒'}`;
    return rtn
}

export function time_diff(time: number, eng = true) {
    return time_diff_sec(Math.round(+new Date() / 1000) - time, eng)
}
