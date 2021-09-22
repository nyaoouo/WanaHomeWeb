<template>
    <div>
        <div class="floating_button">
            <b-btn class="my-2" @click="side_vis=!side_vis" pill size="lg"
            v-b-tooltip.hover.lefttop.dh200="'服务器'">
                <b-icon-menu-button/>
            </b-btn>
            <br/>
            <b-btn class="my-2" @click="$emit('update')" pill size="lg"
            v-b-tooltip.hover.lefttop.dh200="'重载'">
                <b-icon-arrow-clockwise/>
            </b-btn>
            <br/>
            <b-btn class="my-2" @click="$router.push({name:'ServerList'})" pill size="lg"
            v-b-tooltip.hover.lefttop.dh200="'返回列表'">
                <b-icon-arrow-return-left/>
            </b-btn>
        </div>
        <b-sidebar
            v-model="side_vis"
            :title="servers[$route.params.server]"
            backdrop
            shadow
        >
            <b-list-group class="my-3">
                <b-list-group-item button :disabled="$router.currentRoute.name==='State'"
                                   @click="$router.push({name:'State',params:{server:$route.params.server}})"
                >总览
                </b-list-group-item>
                <b-list-group-item v-for="(v,k) in territories" :key="k" button
                                   :disabled="$route.name==='ServerMap' && $route.params.map===k"
                                   @click="$router.push({name:'ServerMap',params:{server:$route.params.server, map:k}})"
                >{{ v.full }}
                </b-list-group-item>
            </b-list-group>
        </b-sidebar>
    </div>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {servers, territories} from "@/libs/WardLandDefine";

@Component
export default class SideBar extends Vue {
    servers = servers
    territories = territories
    side_vis = false
}
</script>

<style scoped>

</style>
