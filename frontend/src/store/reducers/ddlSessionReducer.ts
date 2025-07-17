import { SET_DDL_SESSIONS } from '../actions'

const initialState = {
    ddlSessions: []
}

const ddlSessionReducer = (state = initialState, action: any) => {
    switch (action.type) {
        case SET_DDL_SESSIONS:
            return {
                ddlSessions: action.ddlSessions
            }
        default:
            return state
    }
}

export default ddlSessionReducer 