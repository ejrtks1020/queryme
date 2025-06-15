import React, { useState } from 'react';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    // TODO: 실제 로그인 API 연동
    setTimeout(() => {
      setLoading(false);
      if (email === '' || password === '') {
        setError('이메일과 비밀번호를 입력하세요.');
      } else {
        // 성공 처리 (예시)
        alert('로그인 성공!');
      }
    }, 1000);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded shadow-md w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-6 text-center">로그인</h2>
        <input
          type="email"
          placeholder="이메일"
          className="w-full mb-3 px-3 py-2 border rounded"
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="비밀번호"
          className="w-full mb-3 px-3 py-2 border rounded"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        {error && <div className="text-red-500 text-sm mb-2">{error}</div>}
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
          disabled={loading}
        >
          {loading ? '로그인 중...' : '로그인'}
        </button>
      </form>
    </div>
  );
};

export default Login; 