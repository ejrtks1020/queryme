import { useNavigate } from 'react-router-dom';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="w-full flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-8">홈페이지</h1>
      <button
        onClick={() => navigate('/login')}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        로그인
      </button>
    </div>
  );
} 