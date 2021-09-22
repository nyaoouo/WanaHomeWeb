<template>
    <div style="max-width: 90%;">
        <side-bar @update="update()"/>
        <b-row align-h="between" cols="1" cols-md="2">
            <b-col md="auto">
                <p class="p-2">{{ servers[$route.params.server] }} - {{ territories[$route.params.map].full }}
                    <b-badge>{{ time_diff(last_update, false) }}前</b-badge>
                </p>
            </b-col>
            <b-col md="auto">
                <b-pagination
                    pills
                    align="right"
                    v-model="ward_id"
                    :total-rows="ward_cnt*house_cnt"
                    :per-page="house_cnt"
                ></b-pagination>
            </b-col>
        </b-row>

        <hr/>
        <b-row v-if="ward_id<=house_data.length" cols="2" cols-md="4">
            <b-col v-for="(v,k) in house_data[ward_id-1]" :key="k" class="p-1">
                <b-col :class="'shadow-sm rounded '+(v.owner?'':'onsale')">
                    <b-badge>{{ house_size(v.size) }}</b-badge>
                    <house-label :house="{server: $route.params.server,territory_id: $route.params.map,'ward_id': ward_id-1,'house_id': k}"/>
                    <a v-if="v.owner">{{ v.owner }}</a>
                    <a v-else>{{ v.price }} Gil</a>
                </b-col>

            </b-col>
        </b-row>
    </div>
</template>

<script lang="ts">
import {Component, Vue, Watch} from 'vue-property-decorator';
import SideBar from "@/components/SideBar.vue";
import {get_server_territory_state, HouseData} from "@/axios";
import {time_diff} from "@/libs/Utils";
import {servers, territories, house_cnt, ward_cnt, house_size} from "@/libs/WardLandDefine";
import HouseLabel from "@/components/HouseLabel.vue";

@Component({
    components: {
        SideBar,
        HouseLabel
    }
})

export default class ServerMap extends Vue {
    house_data: HouseData[][] = []
    last_update: number = 0;
    time_diff = time_diff
    servers = servers
    territories = territories
    ward_id = 1
    house_size = house_size
    house_cnt = house_cnt
    ward_cnt = ward_cnt

    @Watch('$route.params.map')
    update() {
        get_server_territory_state(this.$route.params.server, parseInt(this.$route.params.map)).then(data => {
            if (!data) return
            this.last_update = data.last_update
            var temp = []
            for (var i = 0; i < data.state.length; i += house_cnt)
                temp.push(data.state.slice(i, i + house_cnt))
            this.house_data=temp
        })
    }

    mounted() {
        this.update();
    }
}
</script>

<style scoped>
.onsale {
    background-color: rgba(255, 155, 155, 0.5)
}
</style>
