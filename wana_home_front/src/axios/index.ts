import axios from "axios";
import router from "@/router";
import {toast} from "@/libs/toast_bv";

const api = axios.create({
    withCredentials: true,
    timeout: 30000,
    baseURL: "/api/",

});
api.interceptors.response.use((response) => response, (error) => {
    if (error.response) {
        if (error.response.status == 403) {
            router.push({
                name: 'Captcha', query: {
                    key: error.response.data['key'],
                    rtn: router.currentRoute.fullPath
                }
            })
            return
        }
        throw error
    }
});


export interface HouseKey {
    'server': number,
    'territory_id': number,
    'ward_id': number,
    'house_id': number,
}

export interface HouseData {
    'price': number,
    'start_sell': number,
    'size': number,
    'owner': string,
}

export interface HouseFullData extends HouseKey, HouseData {
}

export interface Change {
    'house': HouseKey,
    'event_type': number,
    'param1': string,
    'param2': string,
    'record_time': number,
}


export const get_server_list = (): Promise<{
    'server': number,
    'last_update': number
}[]> => api.get("list/")
    .then(res => res ? res.data.data : undefined)

export const get_server_full_state = (server: string): Promise<{
    'states': { [territory_id: number]: HouseData[] },
    'onsale': HouseFullData[],
    'changes': Change[],
    'last_update': number
}> => api.get("state/", {
    params: {
        'server': server,
        'type': -1
    }
}).then(res => res ? res.data : undefined)

export const get_server_territory_state = (server: string, territory_id: number): Promise<{
    'state': HouseData[],
    'last_update': number
}> => api.get("state/", {
    params: {
        'server': server,
        'type': territory_id
    }
}).then(res => res ? res.data : undefined)

export const get_server_base = (server: string): Promise<{
    'onsale': HouseFullData[],
    'changes': Change[],
    'last_update': number
}> => api.get("state/", {
    params: {
        'server': server,
        'type': 0
    }
}).then(res => res ? res.data : undefined)

export const get_house_data = (server: number, territory_id: number, ward_id: number, house_id: number): Promise<{
    'data': HouseData,
    'changes': Change[]
}> => api.get("house/", {
    params: {
        'server': server,
        'territory_id': territory_id,
        'ward_id': ward_id,
        'house_id': house_id,
    }
}).then(res => res ? res.data : undefined)

export const captcha = (token: string) => api.post("captcha/", {t: token,}).then(res => res.data)

export const sync_ngld = (server: number, territory_id: number, ward_id: number, data: any) => api.post("sync_ngld/", {
    'server': server,
    'territory_id': territory_id,
    'ward_id': ward_id,
    'data': data
}).catch(error=>{
    if(error.response.status == 400){
        toast.show("上传错误，请检查参数")
        console.error(error.response.data)
        return
    }
    throw error
})
