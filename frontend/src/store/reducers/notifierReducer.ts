import { ENQUEUE_SNACKBAR, CLOSE_SNACKBAR, REMOVE_SNACKBAR } from '../actions'

interface Notification {
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
    dismissed?: boolean;
}

interface NotifierState {
    notifications: Notification[];
}

export const initialState: NotifierState = {
    notifications: []
}

interface Action {
    type: string;
    key?: string;
    notification?: any;
    dismissAll?: boolean;
}

const notifierReducer = (state: NotifierState = initialState, action: Action): NotifierState => {
    switch (action.type) {
        case ENQUEUE_SNACKBAR:
            return {
                ...state,
                notifications: [
                    ...state.notifications,
                    {
                        key: action.key || '',
                        ...action.notification
                    }
                ]
            }

        case CLOSE_SNACKBAR:
            return {
                ...state,
                notifications: state.notifications.map((notification) =>
                    action.dismissAll || notification.key === action.key ? { ...notification, dismissed: true } : { ...notification }
                )
            }

        case REMOVE_SNACKBAR:
            return {
                ...state,
                notifications: state.notifications.filter((notification) => notification.key !== action.key)
            }

        default:
            return state
    }
}

export default notifierReducer 