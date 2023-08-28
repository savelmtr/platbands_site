interface LoginData {
  email: string
  password: string
}

interface Detail {
  for: string
  text: string
}

interface SuccessPayload {
  accessToken: string
}


interface ErrorPayload {
  detail: Detail
}

export { LoginData, Detail, SuccessPayload, ErrorPayload }
