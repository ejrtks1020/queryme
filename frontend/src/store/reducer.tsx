// @ts-ignore
import { combineReducers } from 'redux'

// reducer import
import notifierReducer from '@/store/reducers/notifierReducer'
import connectionReducer from '@/store/reducers/connectionReducer'
// ==============================|| COMBINE REDUCER ||============================== //

const reducer = combineReducers({
    notifier: notifierReducer,
    connection: connectionReducer
})

export default reducer
