// 쿠키 값 가져오기 (HttpOnly 쿠키는 접근 불가)
export const getCookie = (name: string) => {
  if (!document.cookie) {
    return null;
  }

  const cookies = document.cookie.split(';');
  
  for (let cookie of cookies) {
    const [cookieName, cookieValue] = cookie.trim().split('=');
    if (cookieName === name) {
      return cookieValue || null;
    }
  }
  
  return null;
};

// 쿠키 삭제
export const deleteCookie = (name: string) => {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
};

// 참고: session_id는 HttpOnly 쿠키이므로 JavaScript에서 접근 불가
// 대신 /auth/me API를 사용하여 인증 상태 확인 