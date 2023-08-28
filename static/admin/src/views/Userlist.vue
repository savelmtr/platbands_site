<template>
  <va-card class="markup-tables mb-8">
    <va-card-title>Статьи</va-card-title>
    <table class="va-table va-table--striped va-table--clickable va-table--hoverable">
      <thead>
      <tr>
          <th>Email</th>
          <th>Username</th>
          <th>Статус</th>
      </tr>
      </thead>
      <tbody>
      <tr
          v-for="user in users"
          :key="user.id"
      >
          <td>{{ user.email }}</td>
          <td>{{ user.username }}</td>
          <td>
          <va-badge
              :text="user.status"
              :color="user.status"
          />
          </td>
      </tr>
      </tbody>
    </table>
  </va-card>
</template>
<script setup lang="ts">
import type { Ref } from 'vue'
import { onMounted, ref } from 'vue'
import { UserInList } from '../_types'
import APIUrls from '../_urls'
import { getToken } from '../_auth';


const users: Ref<UserInList[]> = ref([])

onMounted(async () => {
  let r = await fetch(APIUrls.usersCRUD, {
    headers: {
      Authorization: `Bearer ${getToken()}`
    }
  });
  if (r.ok) {
    users.value = await r.json();
  }
})
</script>