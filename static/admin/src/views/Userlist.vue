<template>
  <div class="flex flex-row">
    <va-card class="grow-0 markup-tables px-10 py-4 relative" v-show="!onUserCreate">
      <div class="flex flex-row my-1 items-center">
        <va-card-title class="grow-0">Пользователи</va-card-title>
        <va-input v-model="searchStr"  class="grow-0" placeholder="Поиск"/>
      </div>
      <table class="va-table va-table--striped va-table--clickable va-table--hoverable">
        <thead>
        <tr>
            <th>Email</th>
            <th>Username</th>
            <th>Статус</th>
            <th>Активирован</th>
        </tr>
        </thead>
        <tbody>
        <tr
            v-for="user in users"
            :key="user.id"
            @click="editUser(user)"
        >
            <td>{{ user.email }}</td>
            <td>{{ user.username }}</td>
            <td> <va-badge :text="roles[user.role]" color="primary"/> </td>
            <td class="flex flex-row justify-center"><va-icon class="grow-0" :name="user.isActive? 'check': 'do_not_disturb_on'" color="primary" /></td>
        </tr>
        </tbody>
      </table>
      <va-pagination
        v-if="page > 1"
        v-model="page"
        :pages="totalPages"
        :visible-pages="4"
      />
      <va-button 
        round color="info"
        size="large" 
        class="absolute right-8 bottom-7" 
        icon="add"
        @click="createUser"
      />
    </va-card>
    <UserEditionForm :show="onUserCreate" :data="editingData" @ok="saveOrUpdate" @cancel="cancelEditor"/>
  </div>
</template>
<script setup lang="ts">
import type { Ref } from 'vue'
import { onMounted, ref, watch } from 'vue'
import { UserCreateScheme, UserInList } from '../_types'
import APIUrls from '../_urls'
import { getToken } from '../_auth';
import { debounce } from 'lodash'
import UserEditionForm from '../components/UserEditionForm.vue'


const users: Ref<UserInList[]> = ref([])
const searchStr = ref('')
const page = ref(1)
const totalPages = ref(0)
const onUserCreate = ref(false)
const editingData: Ref<UserCreateScheme|object> = ref({})

const roles = {
  '0': 'user',
  '1': 'moderator',
  '2': 'admin',
  '3': 'superuser'
}

const getUsers = async () => {
  let params = {page: page.value}
  if (searchStr.value) {
    params['query'] = searchStr.value
  }
  let r = await fetch(
    APIUrls.usersCRUD + '?' + new URLSearchParams(params), {
    headers: {
      Authorization: `Bearer ${getToken()}`
    }
  });
  if (r.ok) {
    let data = await r.json();
    users.value = data.users;
    totalPages.value = data.count; 
  }
}

const debouncedGetUsers = debounce(getUsers, 200);

const createUser = () => {
  editingData.value = {
    id: null,
    email: '',
    username: '',
    role: 0,
    isActive: false,
    password: ''
  };
  onUserCreate.value = true;
}

const cancelEditor = () => onUserCreate.value = false;

const editUser = (user: UserInList) => {
  let newuser = user as UserCreateScheme;
  newuser.password = '';
  editingData.value = newuser;
  onUserCreate.value = true; 
}

const saveOrUpdate = async () => {
  let method = editingData.value.id ? 'PATCH' : 'POST'
  let r = await fetch(
  APIUrls.usersCRUD, {
    method: method,
    headers: {
      Authorization: `Bearer ${getToken()}`,
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify(editingData.value)
  });
  if (r.ok) {
    onUserCreate.value = false;
    await getUsers();
  }
}

onMounted(async () => {
  await getUsers();
})

watch(searchStr, async () => {
  await debouncedGetUsers();
})

watch(page, async () => {
  await getUsers();
})
</script>