export function num_to_byte_array(num: number, pad = 0) {
    var data = [];
    while (num > 0 && data.length < pad) {
        data.push(num & 0xff);
        num >>= 8;
    }
    if (pad > data.length) data = data.concat(Array(pad - data.length).fill(0));
    return data
}

export function ushort_to_bytes(num: number) {
    return num_to_byte_array(num, 2)
}

export function short_to_bytes(num: number) {
    if (num < 0) {
        const data = num_to_byte_array(-num, 2)
        data[3] |= 0x80
        return data
    }
    return num_to_byte_array(num, 2)
}

export function int_to_bytes(num: number) {
    return num_to_byte_array(num >>> 0, 4)
}

export function uint_to_bytes(num: number) {
    return num_to_byte_array(num, 4)
}


export function get_num(buffer: number[], start: number, size: number, signed: boolean) {
    const data = buffer.slice(start, start+size).reverse()
    const sign = signed && data[0] & 0x80
    if (sign) data[0] &= 0x7f
    var ans = 0
    data.forEach(byte => {
        ans <<= 8;
        ans += byte;
    })
    return sign ? -ans : ans;
}

export function get_uint(buffer: number[], start = 0) {
    return get_num(buffer, start, 4, false)
}

export function get_int(buffer: number[], start = 0) {
    return get_num(buffer, start, 4, true)
}

export function get_ushort(buffer: number[], start = 0) {
    return get_num(buffer, start, 2, false)
}

export function get_short(buffer: number[], start = 0) {
    return get_num(buffer, start, 2, true)
}
