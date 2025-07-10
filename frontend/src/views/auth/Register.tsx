import { useNavigate } from 'react-router-dom';
import useApi from '@/hooks/useApi';
import authApi from '@/api/auth';
import { useEffect } from 'react';
import { useState } from 'react';

export default function Register() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const signup = useApi(authApi.signup, {
    showErrorMessage: true
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const target = e.target as typeof e.target & {
      email: { value: string };
      password: { value: string };
      name: { value: string };
    };

    signup.request({
      email: target.email.value,
      password: target.password.value,
      name: target.name.value
    })
  };



  useEffect(() => {
    setLoading(signup.loading)
  }, [signup.loading])

  useEffect(() => {
    if (signup.data) {
      navigate('/login');
    }
  }, [signup.data]);

  return (
    <div className="container" style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      padding: '20px'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '400px',
        padding: '30px',
        border: '1px solid #ddd',
        borderRadius: '8px',
        backgroundColor: 'white',
        boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)'
      }}>
        <h2 className="text-center mb-4">회원가입</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">이름</label>
            <input
              id="name"
              name="name"
              type="text"
              required
              placeholder="이름"
              className="form-control"
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">이메일</label>
            <input
              id="email"
              name="email"
              type="email"
              required
              placeholder="이메일"
              className="form-control"
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
              className="form-control"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password-confirm">비밀번호 확인</label>
            <input
              id="password-confirm"
              name="password-confirm"
              type="password"
              required
              placeholder="비밀번호 확인"
              className="form-control"
            />
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            회원가입
          </button>
          <div className="text-center mt-4">
            <button
              type="button"
              onClick={() => navigate('/login')}
              className="btn"
              style={{ background: 'none', color: '#646cff' }}
            >
              로그인으로 돌아가기
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 