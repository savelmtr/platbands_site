import { Ref, ref } from 'vue'
import APIUrls from './_urls'


const storage: Ref<Storage> = ref( localStorage.getItem('tokenStorage') === 'local'? localStorage : sessionStorage )


const setStorage = (nonTemp: boolean) => {
  if (nonTemp === true) {
    storage.value = localStorage;
    localStorage.setItem('tokenStorage', 'local')
  } else {
    storage.value = sessionStorage;
    localStorage.setItem('tokenStorage', 'session')
  }
}


const setToken = (token: string) => {
  storage.value.setItem('isAuthorized', true);
  storage.value.setItem('accessToken', token);
}


const getToken = (): string => {
  return storage.value.getItem('accessToken')!;
}


const resetToken = () => {
  storage.value.setItem('isAuthorized', false);
  storage.value.setItem('accessToken', '');
}


const isAuthorized = async (): Promise<boolean> => {
  if (storage.value.getItem('isAuthorized')) {
    let r = await fetch(APIUrls.authTest, {
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    });
    if (r.ok) {
      return true
    } else {
      resetToken();
    }
  }
  return false
}

export { storage, getToken, setToken, isAuthorized, setStorage }
