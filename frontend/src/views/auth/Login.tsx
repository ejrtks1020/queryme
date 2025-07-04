import { useNavigate } from 'react-router-dom';
import useApi from '@/hooks/useApi';
import authApi from '@/api/auth';
import { useEffect, useState } from 'react';
import { setUserInfo } from '@/utils/storage.ts';

export default function Login() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const login = useApi(authApi.login, {
    showErrorMessage: true
  })
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const target = e.target as typeof e.target & {
      email: { value: string };
      password: { value: string };
    };
    login.request({
      email: target.email.value,
      password: target.password.value
    })
  };



  useEffect(() => {
    setLoading(login.loading)
  }, [login.loading])

  useEffect(() => {
    if (login.data) {
      // 로그인 성공 시 유저 정보를 로컬스토리지에 저장
      console.log("@@@@@@@@@@@@@@ login.data : ",login.data);
      if (login.data.data) {
        console.log("유저 정보 저장 중:", login.data.data);
        setUserInfo(login.data.data);
        console.log("유저 정보 저장 완료");
        
      } else {
        console.log("login.data.data가 없음");
      }
    }
  }, [login.data, navigate]);

  return (
    <div className="container">
      <h2 className="text-center mb-4">로그인</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">이메일</label>
          <input
            id="email"
            name="email"
            type="email"
            required
            placeholder="이메일"
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">비밀번호</label>
          <input
            id="password"
            name="password"
            type="password"
            required
            placeholder="비밀번호"
          />
        </div>
        <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>
          로그인
        </button>
        <div className="text-center mt-4">
          <button
            type="button"
            onClick={() => navigate('/register')}
            className="btn"
            style={{ background: 'none', color: '#646cff' }}
          >
            회원가입
          </button>
        </div>
      </form>
    </div>
  );
} 