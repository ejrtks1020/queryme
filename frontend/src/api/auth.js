import client from './client'

const login = (body) => client.post(`/auth/login`, body)
const signup = (body) => client.post(`/auth/signup`, body)
const me = () => client.get(`/auth/me`)
const logout = () => client.post(`/auth/logout`)

export default {
    login,
    signup,
    me,
    logout
}
