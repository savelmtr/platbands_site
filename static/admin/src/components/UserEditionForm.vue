<template>
  <va-card v-if="show" class="flex flex-grow-0 p-10" @keyup.esc="emit('cancel')" tabindex="0">
    <va-form class="flex flex-col">
      <va-input
        v-model="data.email"
        :rules="[(v) => (v && v.length > 0) || 'Email обязателен.']"
        label="Электропочта"
        class="mb-6"
        type="email"
        :error="!!emailErrors.length"
        :error-messages="emailErrors"
        ref="emailInput"
      />
      <va-input
        v-model="data.username"
        label="Имя"
        class="mb-6"
      />
      <va-input
        v-model="data.password"
        label="Пароль"
        class="mb-6"
        type="password"
        :error="!!passwordErrors.length"
        :error-messages="passwordErrors"
      />
      <div class="mb-6 flex flex-row flex-grow-0 items-center	">
        <va-select
          v-model="roleValue"
          label="Роль"
          :options="options"
        />
        <va-checkbox v-model="data.isActive" class="ml-4" label="Активирован" />
      </div>
      <div class="flex flex-row flex-grow-0">
        <va-button class="mx-3" @click="sendOK">OK</va-button>
        <va-button @click="emit('cancel')" class="mx-3" preset="secondary">Отмена</va-button>
      </div>
    </va-form>
  </va-card>
</template>
<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue';
import { UserCreateScheme } from '../_types';

const props = defineProps<{
  show: boolean,
  data: UserCreateScheme
}>();
const emit = defineEmits(['cancel', 'ok']);

const options = [
  {
    text: "User",
    value: 0
  },
  {
    text: "Moderator",
    value: 1
  },
  {
    text: "Admin",
    value: 2
  },
  {
    text: "SuperUser",
    value: 3
  },
];
const emailInput = ref();
const roleValue = ref();
const emailErrors = ref<string[]>([]);
const passwordErrors = ref<string[]>([]);
const formReady = computed(() => !emailErrors.value.length || !passwordErrors.value.length);
const emailRe = /^[a-zA-Z_0-9\-]+@[a-zA-Z_0-9\-]+\.\w+$/;

const formCheck = () => {
  emailErrors.value = props.data.email ? [] : ['Электронная почта обязательна'];
  if (!emailErrors.value.length) {
    emailErrors.value = props.data.email.match(emailRe) ? [] : ['Некорректный формат электронной почты'];
  }
  passwordErrors.value = !props.data.id && !props.data.password ? ['При создании пользователя пароль обязателен'] : [];
}

const sendOK = () => {
  if (!formReady.value) return;
  formCheck();
  if (!formReady.value) return;
  emit('ok');
}

watch(() => props.show,() => {
  if (props.show) {
    roleValue.value = options.find(e => e.value === props.data.role);
    nextTick(() => emailInput.value.focus());
  }
})

watch(() => props.data.email, () => {
  emailErrors.value = [];
})
watch(() => props.data.password, () => {
  passwordErrors.value = [];
})

watch(roleValue, () => {
  if (roleValue.value) props.data.role = roleValue.value.value;
})
</script>
