import { useState } from 'react'

export default (apiFunc) => {
    const [data, setData] = useState(null)
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(false)

    const request = async (...args) => {
        setLoading(true)
        try {
            console.log('request', args)
            const result = await apiFunc(...args)
            setData(result.data)
        } catch (err) {
            setError(err || 'Unexpected Error!')
        } finally {
            setLoading(false)
        }
    }

    return {
        data,
        error,
        loading,
        request
    }
}
