// @ts-ignore
import { createStore } from 'redux'
import reducer from '@/store/reducer'

// ==============================|| REDUX - MAIN STORE ||============================== //

const store = createStore(reducer)

export { store }
