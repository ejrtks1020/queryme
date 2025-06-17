import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
// @ts-ignore
import { getUserInfo, setUserInfo, clearAuthData } from '@/utils/storage';
// @ts-ignore
import authApi from '@/api/auth';

interface AuthGuardProps {
  children: React.ReactNode;
  requireAuth?: boolean; // true면 인증 필요, false면 인증시 리다이렉트
}

export default function AuthGuard({ children, requireAuth = true }: AuthGuardProps) {
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        const checkAuth = async () => {
            console.log("checkAuth 실행");
            const userInfo = getUserInfo();
            console.log("저장된 유저정보:", userInfo);

            // 유저정보가 있으면 일단 인증된 것으로 간주
            if (userInfo) {
                console.log("로컬스토리지에 유저정보 있음 - 인증됨으로 설정");
                setIsAuthenticated(true);
                setIsLoading(false);
                return;
            }

            // 유저정보가 없으면 auth/me API로 확인
            try {
                console.log("로컬스토리지에 유저정보 없음 - API 확인");
                const response = await authApi.me();
                console.log("auth/me 응답:", response);
                
                // API 응답이 성공하면 유저정보 저장 (이벤트 발생 안함)
                setUserInfo(response.data.data, false);
                setIsAuthenticated(true);
            } catch (error) {
                console.error('인증 확인 실패:', error);
                // 인증되지 않음
                setIsAuthenticated(false);
            }

            setIsLoading(false);
        };

        checkAuth();
        
        // 유저 정보 변경을 감지하여 인증 상태 업데이트
        const handleUserInfoChange = (event: Event) => {
            const customEvent = event as CustomEvent;
            console.log("유저 정보 변경 감지:", customEvent.detail);
            checkAuth();
        };
        
        window.addEventListener('userInfoChanged', handleUserInfoChange);
        return () => window.removeEventListener('userInfoChanged', handleUserInfoChange);
    }, []);

    useEffect(() => {
        console.log("AuthGuard 상태:", { isLoading, isAuthenticated, requireAuth });
        
        if (!isLoading) {
            if (requireAuth && !isAuthenticated) {
                // 인증이 필요한 페이지인데 인증되지 않은 경우 -> 로그인으로
                console.log("인증 필요 -> 로그인으로 이동");
                navigate('/login', { replace: true });
            } else if (!requireAuth && isAuthenticated) {
                // 인증이 필요하지 않은 페이지(로그인/회원가입)인데 인증된 경우 -> 홈으로
                console.log("인증됨 -> 홈으로 이동");
                navigate('/', { replace: true });
            } else {
                console.log("현재 페이지에 머물기");
            }
        }
    }, [isLoading, isAuthenticated, requireAuth, navigate]);

    // 로딩 중이거나 적절하지 않은 상태라면 로딩 표시
    if (isLoading) {
        return (
        <div style={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '100vh' 
        }}>
            <div>로딩 중...</div>
        </div>
        );
    }

    // 인증 상태가 페이지 요구사항과 맞지 않으면 null 반환 (리다이렉트 진행 중)
    if (requireAuth && !isAuthenticated) {
        return null;
    }

    if (!requireAuth && isAuthenticated) {
        return null;
    }

    return <>{children}</>;
} 