
interface UserInList {
    id: string|null
    email: string
    username: string
    role: number,
    isActive: boolean
}

interface UserCreateScheme {
    id: string|null
    email: string
    username: string
    password?: string
    role: number,
    isActive: boolean
}

export { UserInList, UserCreateScheme }