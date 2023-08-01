import type { NextPage } from 'next'
import Image from 'next/image';
// SWR
import { flaskInstance } from '../../utils/apiClients';
import useSWR, { useSWRConfig } from 'swr'
// React
import { useState } from 'react';
// Material UI
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import FormControlLabel from '@mui/material/FormControlLabel';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import Switch from '@mui/material/Switch';
import Typography from '@mui/material/Typography';
// Material Icons
import CancelTwoToneIcon from '@mui/icons-material/CancelTwoTone';
import CircularProgress from '@mui/material/CircularProgress';
import LinearProgress from '@mui/material/LinearProgress';

const ImageThumbnail = (props) => {
  return (
    <ImageListItem
      component={Button}
      disableRipple
      onClick={props.onClick}
      sx={{
        position: "relative",
        border: "2px solid",
        borderColor: `${props.selected ? '#42A5F5': '#FFF'}`
      }}
    >
      <Image
        loader={() => props.image}
        src={props.image}
        layout='fill'
        objectFit='contain'
      />
      { props.error &&
      <CancelTwoToneIcon
        color="error"
        fontSize="large"
        sx={{ position: "absolute", right: "-18px", top: "-18px" }}/>}
    </ImageListItem>
  )
}

const DemoPage: NextPage = () => {

  // States
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [showHeatmap, setShowHeatmap] = useState(false);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([
    // Use placeholder image
    { "image": "/placeholder4x3.jpg", "heatmap": "/placeholder4x3.jpg", "error": false },
  ]);
  const [error, setError] = useState("");

  // Events
  const inspect = async (e) => {
    setLoading(true);
    try {
      const res = await flaskInstance.get("/api/inspection/ur5demo");
      setData(res.data.results);
    } catch(error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Box sx={{ mb: 3, display: "flex", alignItems: "center" }}>
        <Typography variant="h4" sx={{ flexGrow: 1 }}>Defect Inspection</Typography>
        <FormControlLabel
          control={
            <Switch
              checked={showHeatmap}
              onChange={(e) => setShowHeatmap(e.target.checked)}
            />}
          label="Heatmap"
        />
        <Button variant="outlined" onClick={inspect}>Inspect</Button>
      </Box>

      {
        loading ?
        <>
          <Box sx={{ height: "480px", display: "flex", justifyContent: "center", alignItems: "center" }}>
            <CircularProgress size={60}/>
          </Box>
          <LinearProgress />
        </> :
        <>
          <Box sx={{ height: "600px", position: "relative" }}> {/* 480px */}
            <Image
              loader={() => data[currentImageIndex][`${showHeatmap ? 'heatmap' : 'image'}`]}
              src={data[currentImageIndex][`${showHeatmap ? 'heatmap' : 'image'}`]}
              layout="fill"
              objectFit="contain" />
          </Box>

          <ImageList
            rowHeight={200}
            gap={25}
            sx={{
              py: 2,
              gridAutoFlow: "column",
              gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr)) !important",
              gridAutoColumns: "minmax(250px, 1fr)"
            }}
          >
            {data.map((item, i) => (
              <ImageThumbnail
                key={i}
                image={item.image}
                selected={currentImageIndex == i}
                onClick={() => setCurrentImageIndex(i)}
                error={item.error}
              />
            ))}
          </ImageList>
        </>
      }
    </>
  )
}

export default DemoPage
