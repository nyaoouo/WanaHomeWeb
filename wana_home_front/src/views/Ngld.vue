<template>
    <b-tabs align="center" pills active-tab-class="m-3"
            active-nav-item-class="font-weight-bold"
            style="max-width: calc(100% - 5px);height: calc(100vh - 5px);">
        <b-tab title="记录" active>
            <b-row>
                <b-col>
                    <h3>本地空房记录{{ empty_array.length }}条</h3>
                </b-col>
                <b-col class="text-right">
                    使用音效：
                    <b-form-select v-if="use_alarm" v-model="sound_level" :options="size_options" style="max-width: 150px"/>
                    <b-form-checkbox class="py-1" button :button-variant="use_alarm?'info':'outline-info'" v-model="use_alarm" inline>
                        <b-icon-bell/>
                    </b-form-checkbox>&nbsp;
                    <b-form-select @change="reload_array()" v-model="show_level"
                                   :options="size_options" style="max-width: 150px"/>
                    <b-btn v-b-tooltip.hover title="清除记录"
                           class="mx-2" @click="empty_record={};empty_array=[];" variant="outline-danger">
                        <b-icon-trash/>
                    </b-btn>
                </b-col>
            </b-row>
            <b-table striped hover :items="empty_array" :busy="empty_array.length<1" :fields="on_sale_fields"
                     table-class="text-center" tbody-class="smr">
                <template #cell(record_time)="data" class="text-right">
                    <time-badge :ts="data.value"/>
                </template>
                <template #cell(house)="data" class="text-right">
                    <house-label :house="data.item"/>
                </template>
                <template #cell(price)="data">
                    {{ data.value }} Gil
                </template>
                <template #cell(size)="data">
                    {{ house_size(data.value) }}
                </template>
                <template #table-busy>
                    <div class="text-center my-2">
                        <strong>没有符合条件的空置记录...</strong>
                    </div>
                </template>
            </b-table>
        </b-tab>
        <b-tab title="令牌">
            <b-row>
                <b-col>
                    <h3>已加载令牌：</h3>
                </b-col>
                <b-col class="text-right">
                    <b-form-checkbox v-model="auto_upload" switch>
                        启用自动上传
                    </b-form-checkbox>
                </b-col>
            </b-row>
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
        </b-tab>
    </b-tabs>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {addOverlayListener, removeOverlayListener} from "@/libs/Ngld";
import {sync_ngld} from "@/axios";
import {servers, territories, HouseSimple, house_size} from "@/libs/WardLandDefine";
import {sign} from "@/libs/encrypt"
import HouseLabel from "@/components/HouseLabel.vue";
import TimeBadge from "@/components/TimeBadge.vue";

interface StoreToken {
    [world_id: string]: string
}

interface WardLandInfo {
    land_id: number
    ward_id: number
    territory_id: number
    server: number
    houses: HouseSimple[]
}

interface HouseEmptyData {
    record_time: number
    server: number
    house_id: number
    ward_id: number
    territory_id: number
    price: number
    size: number
}

@Component({
    components: {
        HouseLabel,
        TimeBadge
    }
})
export default class Ngld extends Vue {
    file1: null = null;
    show_input = false;
    sync_token: StoreToken = {}
    servers = servers
    auto_upload = true
    empty_record: { [key: string]: HouseEmptyData } = {}
    empty_array: HouseEmptyData[] = []
    show_level = 0
    sound_level = 1
    house_size = house_size
    on_sale_fields = [
        {
            key: 'size',
            label: '房型',
            sortable: true,
        },
        {
            key: 'house',
            label: '空置房屋'
        },
        {
            key: 'price',
            class: "d-none d-sm-block",
            label: "价钱",
            sortable: true
        },
        {
            key: 'record_time',
            label: '记录时间'
        },
    ]
    size_options = [
        {value: 0, text: '所有'},
        {value: 1, text: 'M,L'},
        {value: 2, text: '只需L'},
    ]
    alarm = new Audio("/alarm.mp3")
    use_alarm = true

    _house_size(price: number) {
        if (price < 4000000)
            return 1
        else if (price <= 20000000)
            return 2
        else
            return 3
    }
    opcode = "292"

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

    reload_array() {
        this.empty_array = []
        for (var key in this.empty_record)
            if (this.empty_record[key].size > this.show_level)
                this.empty_array.push(this.empty_record[key])
    }

    cb(data: any) {
        const current_time = +new Date()
        const line: string[] = data.line;
        if (line[0] !== this.opcode || !line[6].startsWith('0249')) return;
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
        let has_record = false
        for (let i = 0; i < 60; i++) {
            const start_idx = 2 + i * 10;
            let owner = decoder.decode(new Uint32Array(buffer.slice(start_idx + 2, start_idx + 10)))
                .replace(/\u0000+$/, '');
            const price = buffer[start_idx];
            const key = `${ward_land_info.server}|${ward_land_info.territory_id}|${ward_land_info.ward_id}|${ward_land_info.houses.length}`
            const size = this._house_size(price)
            if (!owner) {
                if (size > this.sound_level) has_record = true;
                if (key in this.empty_record) this.empty_record[key].price = price
                else {
                    this.empty_record[key] = {
                        record_time: current_time,
                        house_id: ward_land_info.houses.length,
                        ward_id: ward_land_info.ward_id,
                        territory_id: ward_land_info.territory_id,
                        server: ward_land_info.server,
                        price: price,
                        size: size,
                    }
                }
            } else {
                if (key in this.empty_record) delete this.empty_record[key]
                if (buffer[start_idx + 1] & 0b10000) owner = `《${owner}》`;
            }
            ward_land_info.houses.push({price: price, owner: owner});
        }
        if (has_record && this.use_alarm) this.alarm.play()
        this.reload_array()
        console.log(ward_land_info)
        if (this.auto_upload)
            if (ward_land_info.server in this.sync_token) {
                const sync_data = sign(this.sync_token[ward_land_info.server], ward_land_info.houses)
                sync_ngld(ward_land_info.server, ward_land_info.territory_id, ward_land_info.ward_id, sync_data).then(res => {
                    if (res)
                        console.log(`${servers[ward_land_info.server]} ${territories[ward_land_info.territory_id].short}${ward_land_info.ward_id + 1} 上传成功`)
                }).catch(err => this.$bvToast.toast(err, {
                    title: "上传失败",
                    autoHideDelay: 1000
                }))
            } else {
                this.$bvToast.toast(`未加载 ${servers[ward_land_info.server]} 令牌，不能进行上传`, {
                    autoHideDelay: 1000
                })
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

<style>
.smr td {
    padding-top: 0.3rem;
    padding-bottom: 0.3rem;
}
</style>
