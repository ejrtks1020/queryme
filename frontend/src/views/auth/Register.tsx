import { useNavigate } from 'react-router-dom';
import useApi from '@/hooks/useApi';
import authApi from '@/api/auth';
import { useEffect } from 'react';
import { useState } from 'react';

export default function Register() {
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();
  const signup = useApi(
    authApi.signup
  )

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    signup.request({
      email: e.target.email.value,
      password: e.target.password.value,
      name: e.target.name.value
    })
  };

  useEffect(() => {
    if (signup.error) {
      setErrorMessage(signup.error.message);
      setTimeout(() => setErrorMessage(''), 3000);
    }
  }, [signup.error]);

  useEffect(() => {
    setLoading(signup.loading)
  }, [signup.loading])

  useEffect(() => {
    if (signup.data) {
      navigate('/login');
    }
  }, [signup.data]);

  return (
    <div className="container">
      <h2 className="text-center mb-4">회원가입</h2>
      {errorMessage && (
        <div style={{
          backgroundColor: '#ffcccc',
          color: '#990000',
          padding: '10px',
          marginBottom: '10px',
          borderRadius: '4px',
          textAlign: 'center'
        }}>
          {errorMessage}
        </div>
      )}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">이름</label>
          <input
            id="name"
            name="name"
            type="text"
            required
            placeholder="이름"
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
        <div className="form-group">
          <label htmlFor="password-confirm">비밀번호 확인</label>
          <input
            id="password-confirm"
            name="password-confirm"
            type="password"
            required
            placeholder="비밀번호 확인"
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
  );
} 