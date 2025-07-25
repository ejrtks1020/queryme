import client from '@/api/client'

const createConnection = (data: any) => client.post('/connection/create', data)
const getConnection = (connectionId: string) => client.get(`/connection/get?connection_id=${connectionId}`)
const updateConnection = (data: any) => client.post('/connection/update', data)
const deleteConnection = (data: any) => client.post('/connection/delete', data)
const getConnectionList = () => client.get('/connection/list')
const executeQuery = (data: { connection_id: string; query: string }) => client.post('/connection/execute-query', data)

export default {
    createConnection,
    getConnection,
    updateConnection,
    deleteConnection,
    getConnectionList,
    executeQuery
}