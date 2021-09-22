<template>
    <div style="max-width: 90%;">
        <side-bar @update="update()"/>
        <p class="p-2">{{ servers[$route.params.server] }} - 总览
            <b-badge>{{ time_diff(last_update, false) }}前</b-badge>
        </p>
        <hr/>
        <b-row cols="1" cols-md="2">
            <b-col>
                <b-table striped hover :items="onsale" :busy="onsale.length<1" :fields="on_sale_fields" table-class="text-center">
                    <template #cell(house)="data" class="text-right">
                        <house-label :house="data.item"/>
                    </template>
                    <template #cell(price)="data">
                        {{ data.value }} Gil
                    </template>
                    <template #cell(start_sell)="data">
                        <time-cd-badge :ts="data.value"/>
                    </template>
                    <template #cell(size)="data">
                        {{ house_size(data.value) }}
                    </template>
                    <template #table-busy>
                        <div class="text-center my-2">
                            <strong>没有空置记录...</strong>
                        </div>
                    </template>
                </b-table>
            </b-col>
            <b-col>
                <p>历史记录</p>
                <hr/>
                <b-list-group>
                    <b-list-group-item class="p-1 rounded m-1" v-for="(v,k) in changes" :key="k">
                        <change-event-line house :change="v"/>
                    </b-list-group-item>
                </b-list-group>
            </b-col>

        </b-row>

    </div>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {Change, HouseFullData, get_server_base} from "@/axios";
import ChangeEventLine from "@/components/ChangeEventLine.vue";
import HouseLabel from "@/components/HouseLabel.vue";
import TimeCdBadge from "@/components/TimeCdBadge.vue";
import {house_size, servers, territories} from "@/libs/WardLandDefine";
import SideBar from "@/components/SideBar.vue";
import {time_diff} from "@/libs/Utils";

@Component({
    components: {
        ChangeEventLine,
        HouseLabel,
        TimeCdBadge,
        SideBar,
    }
})
export default class ServerState extends Vue {
    changes: Change[] = [];
    onsale: HouseFullData[] = [];
    last_update: number = 0;
    house_size = house_size
    servers = servers
    time_diff = time_diff

    on_sale_fields = [
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
            key: 'start_sell',
            label: '空置时间',
            sortable: true,
        },
        {
            key: 'size',
            label: '房型',
            sortable: true,
        },
    ]


    update() {
        get_server_base(this.$route.params.server).then(data => {
            if (!data) return;
            this.last_update = data.last_update;
            this.changes = data.changes;
            this.onsale = data.onsale;
        })
    }

    mounted() {
        this.update();
    }
}
</script>

<style>
.list-group-item {
    background-color: rgba(255, 255, 255, 0.3)

}

.list-group {
    max-height: 80vh;
    overflow: auto;
    -webkit-overflow-scrolling: touch;
}
</style>
