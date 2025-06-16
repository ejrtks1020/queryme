import { Outlet } from 'react-router-dom';

function MainLayout() {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: '#f5f5f5'
    }}>
      <Outlet />
    </div>
  );
}

export default MainLayout; 