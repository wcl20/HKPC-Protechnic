import { createTheme, ThemeOptions } from '@mui/material/styles';

const themeOptions: ThemeOptions = {
  palette: {
    mode: 'dark',
    secondary: {
      main: "#50C878",
      light: "#AFE1AF",
      dark: "#008000"
    },
    background: {
      paper: '#202020',
      default: "#303030"
    },
  },
  zIndex: {
    appBar: 1200,
    drawer: 1100,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          "&::-webkit-scrollbar, & *::-webkit-scrollbar": {
            backgroundColor: "#252525",
            borderRadius: 10,
            width: "8px",
            height: "8px"
          },
          "&::-webkit-scrollbar-thumb, & *::-webkit-scrollbar-thumb": {
            borderRadius: 10,
            backgroundColor: "#42A5F5",
          },
          "&::-webkit-scrollbar-thumb:focus, & *::-webkit-scrollbar-thumb:focus": {
            backgroundColor: "#1565C0",
          },
          "&::-webkit-scrollbar-thumb:active, & *::-webkit-scrollbar-thumb:active": {
            backgroundColor: "#1565C0",
          },
          "&::-webkit-scrollbar-thumb:hover, & *::-webkit-scrollbar-thumb:hover": {
            backgroundColor: "#1565C0",
          },
          "&::-webkit-scrollbar-corner, & *::-webkit-scrollbar-corner": {
            backgroundColor: "#1565C0",
          },
        }
      }
    },
    MuiAppBar: {
      styleOverrides: { colorTransparent: {
        background: "rgba(48, 48, 48, 0.9)"
      }}
    },
    MuiListItemIcon: {
      styleOverrides: { root: { minWidth: 35 } },
    },
    MuiListItem: {
      styleOverrides: {
        root: {
          "&.Mui-selected": { color: "#42A5F5" },
          "&.Mui-selected .MuiListItemIcon-root": { color: "#42A5F5" }
        }
      }
    },
    MuiChip: {
      styleOverrides: { root: { borderRadius: 3 }}
    }
  },
};

export default createTheme(themeOptions);
