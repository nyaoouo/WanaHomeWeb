<template>
    <b-badge
        pill :variant="variant"
    >
        {{ str }}
    </b-badge>
</template>

<script lang="ts">
import {Component, Prop, Vue, Watch} from 'vue-property-decorator';
import {is_same_day, date_format} from "@/libs/Utils";

@Component
export default class TimeCdBadge extends Vue {

    @Prop() ts!: number;
    @Prop() variant!: string;
    @Prop() stop!: boolean;
    str: string = '';
    timer: any;

    @Watch('ts')
    reset() {
        this.str = ''
    }

    date_format() {
        if (this.stop !== undefined && this.str) return
        var diff_sec = Math.round(+new Date() / 1000) - this.ts
        var rtn = ''
        if (diff_sec >= 3600) {
            rtn += `${Math.round(diff_sec / 3600)}h `;
            diff_sec %= 3600;
        }
        if (diff_sec >= 60) {
            rtn += `${Math.round(diff_sec / 60)}m `;
            diff_sec %= 60;
        }
        rtn += `${diff_sec}s`;
        this.str = rtn
    }

    mounted() {
        this.date_format();
        this.timer = setInterval(this.date_format, 1000)
    }

    destory() {
        if (this.timer) clearInterval(this.timer)
    }
}
</script>

<style scoped>

</style>
