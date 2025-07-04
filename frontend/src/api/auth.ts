// @ts-ignore
import client from '@/api/client'

const login = (body: any) => client.post(`/auth/login`, body)
const signup = (body: any) => client.post(`/auth/signup`, body)
const me = () => client.get(`/auth/me`)
const logout = () => client.post(`/auth/logout`)

export default {
    login,
    signup,
    me,
    logout
}
