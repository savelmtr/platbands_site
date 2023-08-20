interface LoginData {
  email: string
  password: string
}

interface Detail {
  for: string
  text: string
}

interface Payload {
  detail?: Detail
  accessToken?: string
}

export { LoginData, Detail, Payload }
