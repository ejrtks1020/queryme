import { useRoutes } from 'react-router-dom'

// routes
import MainRoutes from './MainRoutes'


// ==============================|| ROUTING RENDER ||============================== //

export default function Routes() {
    return useRoutes([MainRoutes])
}
