<template>
    <b-badge
        pill
        v-b-tooltip.hover.lefttop.dh200.v-info="date_format(ts,true)"
    >
        {{ date_format(ts) }}
    </b-badge>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
import {is_same_day, date_format} from "@/libs/Utils";

@Component
export default class TimeBadge extends Vue {
    @Prop() ts!: number;
    @Prop() variant!:string;

    date_format(ts:number, full = false) {
        var d = new Date(ts * 1000);
        const pattern = full ? '{H}:{I}:{S} {D}/{M}/{Y}' : is_same_day(d, new Date()) ? '{H}:{I}:{S}' : '{D}/{M}/{Y}';
        return date_format(d, pattern);
    }
}
</script>

<style scoped>

</style>
