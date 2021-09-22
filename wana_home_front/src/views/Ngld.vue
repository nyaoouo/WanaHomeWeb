<template>
    <div style="max-width: 90%;">
        <h3>已加载令牌：</h3>
        <h3>
            <b-badge class="m-1" :variant="k in sync_token?'success':'danger'" v-for="(v,k) in servers" :key="k">
                {{ v }}
            </b-badge>
        </h3>
        <b-btn block variant="info" @click="show_input=!show_input">设置令牌</b-btn>
        <b-modal title="设置令牌" v-model="show_input" centered hide-footer>
            <b-form-file
                v-model="file1"
                :state="Boolean(file1)"
                placeholder="请选取令牌文件"
            ></b-form-file>
            <b-btn class="m-2" :disabled="!file1" @click="save_token()" block>储存</b-btn>
        </b-modal>
    </div>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {addOverlayListener, removeOverlayListener} from "@/libs/Ngld";
import {sync_ngld} from "@/axios";
import {servers, territories} from "@/libs/WardLandDefine";
import {toast} from "@/libs/toast_bv";

declare const Buffer: any;

interface House {
    price: number
    owner: string
}

interface StoreToken {
    [world_id: string]: string
}

interface WardLandInfo {
    land_id: number
    ward_id: number
    territory_id: number
    server: number
    houses: House[]
}

function sign(token: string, data: House[]) {
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

@Component
export default class Ngld extends Vue {
    file1: null = null;
    show_input = false;
    sync_token: StoreToken = {}
    servers = servers

    save_token() {
        const reader = new FileReader();
        reader.addEventListener('load', (event: any) => {
            let load_data: StoreToken = {};
            event.target.result.split('\n').forEach((line: any) => {
                const temp = /(?<server>.+) *= *(?<token>[A-Za-z0-9]*)/.exec(line)
                if (temp) {
                    let gp = (temp.groups as any)
                    const server_id = Object.keys(servers).find((key: any) => servers[key] === gp.server.trim())
                    if (server_id) load_data[server_id] = gp.token
                }
            })
            localStorage.setItem('sync_token', JSON.stringify(load_data))
            this.sync_token = load_data
            this.file1 = null
            this.show_input = false
        });
        reader.readAsText((this.file1 as any));
    }

    cb(data: any) {
        const line: string[] = data.line;
        if (line[0] !== "252" || !line[6].startsWith('0141')) return;
        const buffer = new Uint32Array(line.length);
        line.slice(10).forEach((str, idx) => {
            buffer[idx] = parseInt(str, 16)
        });
        const ward_land_info: WardLandInfo = {
            land_id: buffer[0] & 0xffff,
            ward_id: buffer[0] >> 16,
            territory_id: buffer[1] & 0xffff,
            server: buffer[1] >> 16,
            houses: []
        };
        const decoder = new TextDecoder();
        for (let i = 0; i < 60; i++) {
            const start_idx = 2 + i * 10;
            let owner = decoder.decode(new Uint32Array(buffer.slice(start_idx + 2, start_idx + 10)))
                .replace(/\u0000+$/, '');
            if (buffer[start_idx + 1] & 0b10000) owner = `《${owner}》`;
            ward_land_info.houses.push({price: buffer[start_idx], owner: owner});
        }
        //console.log(ward_land_info)
        if (ward_land_info.server in this.sync_token) {
            const sync_data = sign(this.sync_token[ward_land_info.server], ward_land_info.houses)
            sync_ngld(ward_land_info.server, ward_land_info.territory_id, ward_land_info.ward_id, sync_data).then(res => {
                if (res) toast.show(`${servers[ward_land_info.server]} ${territories[ward_land_info.territory_id].short}${ward_land_info.ward_id + 1} 上传成功`)

            })
        } else {
            toast.show(`未加载 ${servers[ward_land_info.server]} 令牌，不能进行上传`)
        }
    }

    mounted() {
        const data = localStorage.getItem('sync_token')
        if (data) this.sync_token = JSON.parse(data)
        addOverlayListener('LogLine', this.cb);
    }

    beforeDestroy() {
        removeOverlayListener('LogLine', this.cb);
    }
}
</script>

<style scoped>

</style>
