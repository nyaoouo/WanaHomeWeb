<template>
    <div style="max-width: fit-content">
        <div v-if="!loaded">
            <b-spinner/>
        </div>
        <div ref="captcha"/>
    </div>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {captcha} from "@/axios";


export interface ReCAPTCHA {
    execute(opt_widget_id?: string): void;

    render(container: any, parameters: { [key: string]: any }): void;

    reset(opt_widget_id?: string): void;

    getResponse(opt_widget_id?: string): string;
}


declare var grecaptcha: ReCAPTCHA;

@Component
export default class Recaptcha extends Vue {
    servers: string[] = [];
    loaded: boolean = false;

    success_captcha(token: string) {
        captcha(token).then(_ => {
            this.$router.push({path: (this.$route.query.rtn as string)})
        })
    }

    render_captcha() {
        this.loaded = true;
        grecaptcha.render(this.$refs.captcha, {
            'sitekey': this.$route.query.key,
            'callback': this.success_captcha
        });
    }

    mounted() {
        if ('key' in this.$route.query && 'rtn' in this.$route.query) {
            var callback = this.render_captcha
            var checkExist = setInterval(function () {
                if (grecaptcha != undefined) {
                    callback();
                    clearInterval(checkExist);
                }
            }, 100);
        }
    }
}
</script>

<style scoped>

</style>
