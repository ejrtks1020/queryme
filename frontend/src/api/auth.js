import client from './client'

const login = (body) => client.post(`/auth/login`, body)
const signup = (body) => client.post(`/auth/signup`, body)

export default {
    login,
    signup,
}
