import type { NextPage } from 'next'
// React
import { useState } from 'react';
// Material UI
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Slider from '@mui/material/Slider';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';


const LightPage: NextPage = () => {

const [intensity, setIntensity] = useState<number>(30);

  return (
    <>
      <Box sx={{ mb: 3, display: "flex", alignItems: "center" }}>
        <Typography variant="h4" sx={{ flexGrow: 1 }}>Lights</Typography>
      </Box>
        <Box sx={{ width: 200 }}>
            <Stack spacing={2} direction="row" sx={{ mb: 1 }} alignItems="center">
                <Slider 
                    value={intensity} 
                    onChange={(e, newValue) => setIntensity(newValue as number)} 
                />
            </Stack>
            <Button>OK</Button>
        </Box>
    </>
  )
}

export default LightPage