import axios from 'axios'
import { baseURL } from '@/store/constant'

const apiClient = axios.create({
    baseURL: `${baseURL}`,
    headers: {
        'Content-type': 'application/json',
    }
})

// apiClient.interceptors.request.use(function (config) {

//     return config
// })

export default apiClient
