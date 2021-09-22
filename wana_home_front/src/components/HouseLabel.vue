<template>
    <b-btn class="p-1" variant="link" @click="show()">
        {{ format() }}
        <b-modal v-if="m_show && house_data" :title="format()" v-model="m_show" hide-footer centered>
            <b-table-simple hover small stacked>
                <b-tbody>
                    <b-tr>
                        <b-th stacked-heading="服务器">
                            {{ servers[house.server] }}
                        </b-th>
                        <b-td stacked-heading="地图">
                            <b-btn
                                @click="$router.push({name:'ServerMap',params:{'server':house.server, 'map':house.territory_id}}).catch(_=>0)"
                                variant="link" class="p-0">
                                {{ territories[house.territory_id].full }}
                            </b-btn>
                        </b-td>
                        <b-td stacked-heading="区号">{{ house.ward_id + 1 }}</b-td>
                        <b-td stacked-heading="房号">{{ house.house_id + 1 }}</b-td>
                    </b-tr>
                    <b-tr>
                        <b-td stacked-heading="房型">
                            {{ house_size(house_data.size) }}
                        </b-td>
                        <b-th v-if="house_data.owner" stacked-heading="房主">
                            {{ house_data.owner }}
                        </b-th>
                        <b-td v-if="!house_data.owner" stacked-heading="价钱">
                            {{ house_data.price }}Gil
                        </b-td>
                        <b-td v-if="!house_data.owner" stacked-heading="已空置">
                            <time-cd-badge :ts="house_data.start_sell"/>
                        </b-td>
                    </b-tr>
                </b-tbody>
            </b-table-simple>
            <div v-if="changes.length>0">
                <h5>历史记录</h5>
                <b-list-group>
                    <b-list-group-item class="p-1 rounded m-1" v-for="(v,k) in changes" :key="k">
                        <change-event-line :change="v"/>
                    </b-list-group-item>
                </b-list-group>
            </div>

        </b-modal>
    </b-btn>
</template>

<script lang="ts">
import {Component, Vue, Prop} from 'vue-property-decorator';
import {Change, get_house_data, HouseData, HouseKey} from "@/axios";
import {zero_pad} from "@/libs/Utils";
import {house_size, servers, territories} from "@/libs/WardLandDefine";
import TimeCdBadge from "@/components/TimeCdBadge.vue";

@Component({
    components: {TimeCdBadge,},
})
export default class HouseLabel extends Vue {
    @Prop() house!: HouseKey;
    m_show = false;
    house_data!: HouseData;
    changes!: Change[];
    territories = territories
    servers = servers

    format() {
        return territories[this.house.territory_id].short +
            ` ${zero_pad(this.house.ward_id + 1, 2)}-${zero_pad(this.house.house_id + 1, 2)}`
    }

    house_size = house_size

    beforeCreate() {
        (this.$options.components as any)['ChangeEventLine'] = () => import("@/components/ChangeEventLine.vue")
    }

    show() {
        get_house_data(this.house.server, this.house.territory_id, this.house.ward_id, this.house.house_id).then(data => {
            if (!data) return;
            this.house_data = data.data;
            this.changes = data.changes;
            this.m_show = true;
        })
    }
}
</script>

<style scoped>

</style>
