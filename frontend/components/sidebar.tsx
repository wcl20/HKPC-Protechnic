import Link from 'next/link';
import { useRouter } from 'next/router';
// Material UI
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';
import Toolbar from '@mui/material/Toolbar';
// Icons
import BrokenImageIcon from '@mui/icons-material/BrokenImage';
import HomeIcon from '@mui/icons-material/Home';
import LightModeIcon from '@mui/icons-material/LightMode';

function LinkItem(props) {
  const router = useRouter();
  const isSelected = router.pathname == props.path;

  return (
    <Link href={props.path} passHref>
      <ListItem button component="a" selected={isSelected}>
        <ListItemIcon>{props.icon || <ScienceIcon />}</ListItemIcon>
        <ListItemText primary={props.label} />
      </ListItem>
    </Link>
  )
}

export default function SideBar(props) {

  return(
    <Drawer
      variant="permanent"
      sx={{
        width: 240,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: 240, boxSizing: 'border-box' },
      }}
    >
      <Toolbar />
      <List subheader={<ListSubheader>GENERAL</ListSubheader>}>
        <LinkItem path="/" label="Overview" icon={<HomeIcon />} />
      </List>
      <Divider />
      <List subheader={<ListSubheader>APPS</ListSubheader>}>
        <LinkItem path="/apps/demo" label="Defect Inspection" icon={<BrokenImageIcon />} />
        <LinkItem path="/apps/light" label="Light" icon={<LightModeIcon />} />
      </List>
    </Drawer>
  )
}
