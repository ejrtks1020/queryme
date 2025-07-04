import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Alert, Space } from 'antd';
import { closeSnackbar, removeSnackbar } from '@/store/actions';

interface RootState {
    notifier: {
        notifications: Array<{
        key: string;
        message: string;
        options: {
            variant: string;
            autoHideDuration: number;
            anchorOrigin: {
            vertical: string;
            horizontal: string;
            };
        };
        dismissed: boolean;
        }>;
    };
}

export default function GlobalNotification() {
    const dispatch = useDispatch();
    const notifications = useSelector((state: RootState) => state.notifier.notifications);

    useEffect(() => {
        // 자동으로 알림을 제거하는 타이머 설정
        notifications.forEach((notification) => {
        if (!notification.dismissed) {
            setTimeout(() => {
            dispatch(closeSnackbar(notification.key));
            setTimeout(() => {
                dispatch(removeSnackbar(notification.key));
            }, 300);
            }, notification.options?.autoHideDuration || 5000);
        }
        });
    }, [notifications, dispatch]);

    // 표시할 알림들만 필터링
    const activeNotifications = notifications.filter(notification => !notification.dismissed);

    if (activeNotifications.length === 0) {
        return null;
    }

    return (
        <div
        style={{
            position: 'fixed',
            top: '20px',
            right: '20px',
            zIndex: 9999,
            maxWidth: '400px',
            width: '100%'
        }}
        >
        <Space direction="vertical" style={{ width: '100%' }}>
            {activeNotifications.map((notification) => {
            let alertType: 'error' | 'success' | 'info' | 'warning' = 'info';
            
            switch (notification.options?.variant) {
                case 'error':
                alertType = 'error';
                break;
                case 'success':
                alertType = 'success';
                break;
                case 'warning':
                alertType = 'warning';
                break;
                default:
                alertType = 'info';
            }

            return (
                <Alert
                key={notification.key}
                message={notification.message}
                type={alertType}
                showIcon
                closable
                onClose={() => {
                    dispatch(closeSnackbar(notification.key));
                    setTimeout(() => {
                    dispatch(removeSnackbar(notification.key));
                    }, 300);
                }}
                style={{
                    marginBottom: '8px',
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                    borderRadius: '6px'
                }}
                />
            );
            })}
        </Space>
        </div>
    );
} 