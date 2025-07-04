import { SET_CONNECTIONS } from '../actions'

const initialState = {
    connections: []
}

const connectionReducer = (state = initialState, action: any) => {
    switch (action.type) {
        case SET_CONNECTIONS:
            return {
                connections: action.connections
            }
        default:
            return state
    }
}

export default connectionReducer