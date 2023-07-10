import Image from 'next/image'
// Material UI
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import SvgIcon from '@mui/material/SvgIcon';
import Toolbar from '@mui/material/Toolbar';
// Icons
import logoIcon from '../public/logo.svg';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

export default function NavBar(props) {
  return (
    <AppBar
      position="fixed"
      color="transparent"
    >
      <Toolbar>
        <Image src="/flairlogo.png" alt="Logo" width={160} height={40} />
        <Box sx={{ flexGrow: 1 }} />
        <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
          <IconButton size="large" edge="end" color="inherit">
            <AccountCircleIcon />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  )
}
