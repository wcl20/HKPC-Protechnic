import * as React from 'react';
import type { AppProps } from 'next/app'
// Material UI
import { CacheProvider, EmotionCache } from '@emotion/react';
import { ThemeProvider, CssBaseline, createTheme } from '@mui/material';
import createEmotionCache from '../utils/createEmotionCache';
import darkTheme from '../styles/themes/darkTheme';
import '../styles/globals.css';
// Layouts
import MainLayout from '../layouts/mainLayout';

interface ExtendedAppProps extends AppProps {
  emotionCache?: EmotionCache;
}

const clientSideEmotionCache = createEmotionCache();

function MyApp({
  Component, pageProps, emotionCache=clientSideEmotionCache
}: ExtendedAppProps) {

  return (
    <CacheProvider value={emotionCache}>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <MainLayout>
          <Component {...pageProps} />
        </MainLayout>
      </ThemeProvider>
    </CacheProvider>
  )
}

export default MyApp
