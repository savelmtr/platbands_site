<template>  
  <div class="app-layout__content" v-if="showContent">
    <div class="app-layout__sidebar-wrapper">
      <Sidebar />
    </div>
    <div class="app-layout__page" v-if="showContent">
      <div class="p-2 md:px-6 md:py-9">
        <router-view />
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import Sidebar from '../components/Sidebar.vue'
import { ref } from 'vue';
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'DefaultLayout',
  components: { Sidebar }
}
</script>
<script setup lang="ts">

  const router = useRouter()
  const store = useStore()
  const showContent = ref(false)

  if (!localStorage.getItem('accessToken')) {
    router.push({'name': 'login'})
  } else {
    showContent.value = true
  }
  console.log(localStorage.getItem('accessToken'))
</script>
<style lang="scss">
  $mobileBreakPointPX: 640px;
  $tabletBreakPointPX: 768px;

  .app-layout {
    height: 100vh;
    display: flex;
    flex-direction: column;
    &__navbar {
      min-height: 4rem;
    }

    &__content {
      display: flex;
      height: 100vh; // calc(100vh - 4rem);
      flex: 1;

      @media screen and (max-width: $tabletBreakPointPX) {
        height: calc(100vh - 6.5rem);
      }

      .app-layout__sidebar-wrapper {
        position: relative;
        height: 100%;
        background: #ffffff;

        @media screen and (max-width: $tabletBreakPointPX) {
          &:not(.minimized) {
            width: 100%;
            height: 100%;
            position: fixed;
            top: 0;
            z-index: 999;
          }

          .va-sidebar:not(.va-sidebar--minimized) {
            .va-sidebar__menu {
              padding: 0;
            }
          }
        }
      }
    }
    &__page {
      flex-grow: 2;
      overflow-y: scroll;
    }
  }
</style>
