<template>
  <div class="auth-layout grid grid-cols-12 content-center">
    <div class="flex col-span-12 p-4 justify-center">
      <router-link class="text-2xl text-blue-600 py-5 justify-center flex" to="/">
        Вход в административную панель
      </router-link>
    </div>

    <div class="flex justify-center col-span-12 p-4">
      <va-card class="auth-layout__card">
        <va-card-content>
          <div class="p-3">
            <form @submit.prevent="onsubmit" class="flex flex-col">
              <va-input
                v-model="email"
                class="mb-4"
                type="email"
                label="Электронная почта"
                :error="!!emailErrors.length"
                :error-messages="emailErrors"
              />

              <va-input
                v-model="password"
                class="mb-4"
                type="password"
                label="Пароль"
                :error="!!passwordErrors.length"
                :error-messages="passwordErrors"
              />

              <div style="display: flex; align-items: center; justify-content: space-between;">
                  <va-button round type="submit" class="my-0" @click="onsubmit">Войти</va-button>
                  <router-link class="ml-1 va-link" :to="{ name: 'recover-password' }">
                    Восстановить пароль
                  </router-link>
              </div>
            </form>
          </div>
        </va-card-content>
      </va-card>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { computed, ref, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import APIUrls from '@/_urls.js'
  import { useStore } from 'vuex'

  const email = ref('')
  const password = ref('')
  const keepLoggedIn = ref(false)
  const emailErrors = ref<string[]>([])
  const passwordErrors = ref<string[]>([])
  const router = useRouter()
  const store = useStore()

  const formReady = computed(() => !emailErrors.value.length && !passwordErrors.value.length)

  class LoginData {
    email: string
    password: string

    constructor(email: string, password: string) {
      this.email = email
      this.password = password
    }
  }

  class Detail {
    for: string
    text: string
  }

  interface Payload {
    detail?: Detail
    accessToken?: string
  }

  async function onsubmit() {
    if (!formReady.value) return

    emailErrors.value = email.value ? [] : ['Email is required']
    passwordErrors.value = password.value ? [] : ['Password is required']

    if (emailErrors.value.length || passwordErrors.value.length) return
    let login_result = await login(new LoginData(email.value, password.value))
    if (login_result === true) {
      router.push({ name: 'admin' })      
    }
  }

  async function login(data: LoginData): Promise<boolean> {
    let request = await fetch(APIUrls.login, {
      method: 'POST',
      mode: "cors",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data),
    })
    let payload: Payload;
    if (request.ok) {
      payload = await request.json()
      if (payload.accessToken) {
        localStorage.setItem('accessToken', payload.accessToken);
      }
      console.log(store)
      return true
    } else if (request.status == 401) {
      payload = await request.json()
      if (payload.detail) {
        switch (payload.detail.for) {
          case 'email':
            emailErrors.value = [payload.detail.text]
            passwordErrors.value = []
            break
          case 'password':
            emailErrors.value = []
            passwordErrors.value = [payload.detail.text]
        }
      }
    } else {
      console.log(`Ошибка при запросе к эндпойнту ${APIUrls.login}. Статус: ${request.status}`)
    }
    return false
  }

  watch(email, (newEmail) => {
    emailErrors.value = []
  })

  watch(password, (newPass) => {
    passwordErrors.value = []
  })
</script>

<style lang="scss">
  .auth-layout {
    min-height: 100vh;
    background-image: linear-gradient(to right, var(--va-background-primary), var(--va-white));

    &__card {
      width: 100%;
      max-width: 600px;
    }
  }
</style>
