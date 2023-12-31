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
              
              <va-checkbox v-model="keepLoggedIn" class="mb-4" label="Запомнить меня" />
              <div class="flex items-center justify-between">
                  <va-button round type="submit" class="my-0 grow-0" @click="onsubmit">Войти</va-button>
                  <router-link class="ml-1 va-link grow-0" :to="{ name: 'recover-password' }">
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
import { LoginData, SuccessPayload, ErrorPayload } from '../../interfaces'
import { setStorage, setToken, storage } from '../../_auth';
  
  const email = ref('')
  const password = ref('')
  const keepLoggedIn = ref(localStorage.getItem('tokenStorage'))
  const emailErrors = ref<string[]>([])
  const passwordErrors = ref<string[]>([])
  const router = useRouter()


  const formReady = computed(() => !emailErrors.value.length && !passwordErrors.value.length)

  async function onsubmit() {
    if (!formReady.value) return

    emailErrors.value = email.value ? [] : ['Email is required']
    passwordErrors.value = password.value ? [] : ['Password is required']

    if (!formReady.value) return

    setStorage(keepLoggedIn.value);
    let login_result = await login({'email': email.value, 'password': password.value})
    if (login_result === true) {
      router.push({ name: 'admin' })      
    }
  }

  function setOnLoginError(payload: ErrorPayload) {
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

  async function login(data: LoginData): Promise<boolean> {
    let request = await fetch(APIUrls.login, {
      method: 'POST',
      mode: "cors",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data),
    })
    let payload: SuccessPayload | ErrorPayload;
    if (request.ok) {
      payload = await request.json() as SuccessPayload
      setToken(payload.accessToken)
      return true
    } else if (request.status == 401) {
      payload = await request.json() as ErrorPayload
      setOnLoginError(payload)
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
