<template>
    <va-navbar
    color="secondary"
    style="padding: 1rem"

  >
    <template #left>
        <va-icon
            class="mr-2"
            name="menu"
            size="2rem"
            @click="$store.commit('toggleSidebar')"
        />
    </template>
    <template #right>
      <!-- <va-navbar-item>Dashboard</va-navbar-item>
      <va-navbar-item>Reports</va-navbar-item>
      <va-navbar-item>Users</va-navbar-item>
      <va-navbar-item>
        <va-icon
          name="mdi-magnify"
          color="textInverted"
        />
      </va-navbar-item>
      <va-navbar-item>
        <va-icon
          name="mdi-account-circle-outline"
          color="textInverted"
        />
      </va-navbar-item> -->
    </template>
  </va-navbar>
</template>
<script>
export default {
    name: 'Header'
}
</script>
