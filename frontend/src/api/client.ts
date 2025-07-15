import axios from 'axios'
import { baseURL } from '@/store/constant'
import { clearAuthData } from '@/utils/storage';
const apiClient = axios.create({
    baseURL: `${baseURL}`,
    headers: {
        'Content-type': 'application/json',
    },
    withCredentials: true,
})

// apiClient.interceptors.request.use(function (config) {

//     return config
// })

apiClient.interceptors.response.use(
    (response) => {
        // console.log('@@@@@@@@@@@@@@@@200 response', response)
        return response
    },
    (error) => {
        if (error.response?.status === 401) {
            // 세션 만료시 자동으로 로그아웃 처리
            // console.log('@@@@@@@@@@@@@@@@401 error')
            clearAuthData();
            // window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default apiClient
