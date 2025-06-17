// 유저 정보 저장
export const setUserInfo = (userInfo, triggerEvent = true) => {
  localStorage.setItem('user_info', JSON.stringify(userInfo));
  // 커스텀 이벤트 발생으로 AuthGuard에게 알림 (선택적)
  if (triggerEvent) {
    window.dispatchEvent(new CustomEvent('userInfoChanged', { detail: userInfo }));
  }
};

// 유저 정보 가져오기
export const getUserInfo = () => {
  const userInfo = localStorage.getItem('user_info');
  return userInfo ? JSON.parse(userInfo) : null;
};

// 유저 정보 삭제
export const removeUserInfo = () => {
  localStorage.removeItem('user_info');
};

// 모든 인증 관련 데이터 삭제
export const clearAuthData = () => {
  localStorage.removeItem('user_info');
  // 다른 인증 관련 데이터가 있다면 여기에 추가
  // 커스텀 이벤트 발생으로 AuthGuard에게 알림
  window.dispatchEvent(new CustomEvent('userInfoChanged', { detail: null }));
};

// 로그아웃 (clearAuthData와 동일하지만 명시적)
export const logout = () => {
  clearAuthData();
}; 