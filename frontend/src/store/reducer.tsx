// @ts-ignore
import { combineReducers } from 'redux'

// reducer import
import notifierReducer from '@/store/reducers/notifierReducer'
import connectionReducer from '@/store/reducers/connectionReducer'
import ddlSessionReducer from '@/store/reducers/ddlSessionReducer'
// ==============================|| COMBINE REDUCER ||============================== //

const reducer = combineReducers({
    notifier: notifierReducer,
    connection: connectionReducer,
    ddlSession: ddlSessionReducer
})

export default reducer
