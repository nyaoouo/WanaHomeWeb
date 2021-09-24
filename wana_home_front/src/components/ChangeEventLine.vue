<template>
    <a>
        <time-badge :ts="change.record_time" variant="info"/>
        <house-label v-if="!house" :house="change.house"/>
        <a class="d-md-none"><br/></a>
        <a v-if="change.event_type==='change_owner'">
            持有者从
            <b-badge>{{ change.param1 }}</b-badge>
            变更为
            <b-badge>{{ change.param2 }}</b-badge>
        </a>
        <a v-else-if="change.event_type==='start_selling'">
            以
            <b-badge>{{ change.param2 }}Gil</b-badge>
            开始售出（前持有人
            <b-badge>{{ change.param1 }}</b-badge>
            ）
        </a>
        <a v-else-if="change.event_type==='price_reduce'">
            从
            <b-badge>{{ change.param1 }}Gil</b-badge>
            降价到
            <b-badge>{{ change.param2 }}Gil</b-badge>
        </a>
        <a v-else-if="change.event_type==='sold'">
            被
            <b-badge>{{ change.param1 }}</b-badge>
            购入
            <a v-if="change.param2">（历时<b-badge>{{time_fmt(change.param2)}}</b-badge>）</a>
        </a>
        <a v-else-if="change.event_type='price_refresh'">
            价格/cd 刷新
        </a>。
    </a>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
import HouseLabel from "@/components/HouseLabel.vue";
import TimeBadge from "@/components/TimeBadge.vue";
import {Change} from "@/axios";
import {time_diff_sec} from "@/libs/Utils";

@Component({
    components: {
        HouseLabel,
        TimeBadge,
    }
})
export default class ChangeEventLine extends Vue {
    @Prop() change!: Change;
    @Prop({default: () => '1'}) house!: string;

    time_fmt(val: string) {
        return time_diff_sec(parseInt(val),false)
    }
}
</script>

<style scoped>

</style>
