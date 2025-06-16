// MNC //////
import { SET_WORKFLOW_ID, SET_USER_TOKEN } from '../actions'


export const initialState = {
    workflowId: null,
    userToken: null
}

const workflowReducer = (state = initialState, action) => {
    switch (action.type) {
        case SET_WORKFLOW_ID:
            return {
              ...state,
              workflowId : action.workflowId
            }
        case SET_USER_TOKEN:
            return {
                ...state,
                userToken : action.userToken
            }            
        default:
            return state
    }
}

export default workflowReducer
