// Material UI
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
// Components
import NavBar from '../components/navbar';
import SideBar from '../components/sidebar';

export default function MainLayout({ children }) {
  return (
    <Box sx={{ display: 'flex', overflowX: "hidden" }}>
      <NavBar />
      <SideBar />
      <Box component="main" sx={{ flexGrow: 1, p: 3, width: "calc(100vw - 240px)" }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  )
}
