import client from '@/api/client'
import { baseURL } from '@/store/constant'
import { clearAuthData } from '@/utils/storage';

const query = (data: any) => client.post('/nl2sql/query', data)
const queryStream = (params: any, onChunk: any, onDone: any, onError: any) => {
    const url = '/nl2sql/query-stream'
    fetch(baseURL + url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        },
        credentials: 'include',
        body: JSON.stringify(params)
        })
        .then(response => {
            if (response.status === 401) {
                clearAuthData();
            }
            if (!response.body) throw new Error('No response body')
            const reader = response.body.getReader()
            const decoder = new TextDecoder()
            let result = ''
            function read() {
            reader.read().then(({ done, value }) => {
                if (done) {
                if (onDone) onDone(result)
                return
                }
                const chunk = decoder.decode(value, { stream: true }).replace(/^data: /, '')
                result += chunk
                if (onChunk) onChunk(chunk)
                read()
            }).catch(err => {
                if (onError) onError(err)
            })
            }
            read()
        })
        .catch(err => {
            if (onError) onError(err)
        })
    }

export default {
    query,
    queryStream
}