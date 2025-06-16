import { useNavigate } from 'react-router-dom';
import useApi from '@/hooks/useApi';
import authApi from '@/api/auth';
import { useEffect, useState } from 'react';

export default function Login() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const login = useApi(
    authApi.login
  )
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login.request({
      email: e.target.email.value,
      password: e.target.password.value
    })
  };

  useEffect(() => {
    if (login.error) {
      setErrorMessage(login.error.message);
      setTimeout(() => setErrorMessage(''), 3000);
    }
  }, [login.error]);

  useEffect(() => {
    setLoading(login.loading)
  }, [login.loading])

  useEffect(() => {
    if (login.data) {
      navigate('/');
    }
  }, [login.data]);

  return (
    <div className="container">
      <h2 className="text-center mb-4">로그인</h2>
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