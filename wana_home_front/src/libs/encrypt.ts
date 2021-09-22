import {House} from "@/libs/WardLandDefine";

declare const Buffer: any;

export function sign(token: string, data: House[]) {
    let new_data = Array(data.length)
    data.forEach((house, idx) => {
        new_data[idx] = [house.owner, house.price]
    })
    if (!token) return new_data
    const encoder = new TextEncoder()
    const token_bytes = encoder.encode(token)
    let data_bytes = encoder.encode(JSON.stringify(new_data))
    for (let i = 0; i < data_bytes.length; i++) data_bytes[i] = data_bytes[i] ^ token_bytes[i % token_bytes.length]
    return Buffer.from(data_bytes).toString('base64')
}
