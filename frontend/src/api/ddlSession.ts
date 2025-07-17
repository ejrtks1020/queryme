import client from '@/api/client'

const createSession = (data: any) => client.post('/ddl-session/create', data)
const getSession = (sessionId: string) => client.get(`/ddl-session/get?session_id=${sessionId}`)
const updateSession = (data: any) => client.post('/ddl-session/update', data)
const deleteSession = (data: any) => client.post('/ddl-session/delete', data)
const getSessionList = () => client.get('/ddl-session/list')

export default {
    createSession,
    getSession,
    updateSession,
    deleteSession,
    getSessionList
} 