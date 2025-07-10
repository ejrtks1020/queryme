import { useState } from 'react'
import { useDispatch } from 'react-redux'
import { enqueueSnackbar } from '@/store/actions'

interface UseApiOptions {
    showSuccessMessage?: boolean;
    successMessage?: string;
    showErrorMessage?: boolean;
}


// // 기본 사용 (에러만 표시)
// const api = useApi(apiFunction);

// // 성공 메시지도 표시
// const api = useApi(apiFunction, {
//   showSuccessMessage: true,
//   successMessage: '성공적으로 완료되었습니다.'
// });

// // 에러 메시지 비활성화
// const api = useApi(apiFunction, {
//   showErrorMessage: false
// });
export default (apiFunc: any, options: UseApiOptions = {}) => {
    const [data, setData] = useState<any>(null)
    const [error, setError] = useState<any>(null)
    const [loading, setLoading] = useState(false)
    const dispatch = useDispatch()

    const {
        showSuccessMessage = false,
        successMessage = '요청이 성공적으로 완료되었습니다.',
        showErrorMessage = true
    } = options

    const request = async (...args: any[]) => {
        setLoading(true)
        try {
            const result = await apiFunc(...args)
            setData(result.data)
            
            // 성공 메시지 표시
            if (showSuccessMessage) {
                dispatch(enqueueSnackbar({
                    message: successMessage,
                    options: {
                        variant: 'success',
                        autoHideDuration: 3000,
                        anchorOrigin: {
                            vertical: 'top',
                            horizontal: 'right'
                        }
                    }
                }))
            }
        } catch (err: any) {
            setError(err || 'Unexpected Error!')
            
            // 에러 메시지 표시 (기본적으로 활성화)
            if (showErrorMessage) {
                // 에러 메시지 추출 및 전역 토스트 알림 표시
                let errorMessage = '알 수 없는 오류가 발생했습니다.'
                
                if (err?.response?.data?.message) {
                    // 서버에서 반환한 에러 메시지
                    errorMessage = err.response.data.message
                } else if (err?.response?.data?.detail) {
                    // FastAPI 스타일 에러 메시지
                    errorMessage = err.response.data.detail
                } else if (err?.message) {
                    // JavaScript 에러 메시지
                    errorMessage = err.message
                } else if (err?.response?.status) {
                    // HTTP 상태 코드 기반 에러 메시지
                    switch (err.response.status) {
                        case 400:
                            errorMessage = '잘못된 요청입니다.'
                            break
                        case 401:
                            errorMessage = '인증이 필요합니다.'
                            break
                        case 403:
                            errorMessage = '접근 권한이 없습니다.'
                            break
                        case 404:
                            errorMessage = '요청한 리소스를 찾을 수 없습니다.'
                            break
                        case 500:
                            errorMessage = '서버 내부 오류가 발생했습니다.'
                            break
                        default:
                            errorMessage = `오류가 발생했습니다. (${err.response.status})`
                    }
                } else if (err?.code === 'NETWORK_ERROR' || err?.code === 'ERR_NETWORK') {
                    errorMessage = '네트워크 연결을 확인해주세요.'
                }
                console.log('@@@@@@@@@@@@@@@@@ errorMessage', errorMessage)
                dispatch(enqueueSnackbar({
                    message: errorMessage,
                    options: {
                        variant: 'error',
                        autoHideDuration: 5000,
                        anchorOrigin: {
                            vertical: 'top',
                            horizontal: 'right'
                        }
                    }
                }))
            }
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
