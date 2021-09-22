<template>
    <div style="max-width: 90%;width: fit-content;">
        <b-row align-h="between" cols="2">
            <b-col md="auto">
                <p>此处应有标题</p>
            </b-col>
            <b-col class="text-right" md="auto">
                <b-btn size="sm" variant="outline-info" @click="update()">
                    <b-icon-arrow-clockwise/>
                </b-btn>
            </b-col>
        </b-row>
        <b-row cols="1" cols-md="2">
            <b-col class="text-center">
                此处应有文字
            </b-col>
            <b-col>
                <b-col v-for="dc in dc_server" :key="dc.dc_name" class="shadow-sm rounded m-2 p-2">
                    {{ dc.dc_name }}
                    <div>
                        <b-btn class="m-1" v-for="(w_name,w_id) in dc.servers"
                               :key="w_id" size="sm" variant="success" :disabled="!(w_id in servers)"
                               v-b-tooltip.hover.top :title="`最近更新：${time_diff(servers[w_id],false)}前`"
                               @click="$router.push({name:'State',params:{server:w_id}})">
                            {{ w_name }}
                            <b-badge v-if="w_id in servers">{{ time_diff(servers[w_id]) }}</b-badge>
                        </b-btn>
                    </div>
                </b-col>
            </b-col>
        </b-row>
    </div>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {get_server_list} from "@/axios";
import {dc_server} from "@/libs/WardLandDefine";
import {time_diff} from "@/libs/Utils";

@Component({
    components: {
    }
})
export default class ServerList extends Vue {
    servers: { [id: number]: number } = {};
    dc_server = dc_server

    time_diff=time_diff

    update() {
        get_server_list().then(res => {
            if (!res) return;
            this.servers = {};
            for (var server of res)
                this.servers[server.server] = server.last_update;
        });
    }

    mounted() {
        this.update();
    }
}
</script>

<style scoped>
.list_dc {
    background-color: rgba(255, 255, 255, 0.5)
}
</style>
