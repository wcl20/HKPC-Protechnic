import type { NextPage } from 'next'
// React
import { useState, useEffect, useRef } from 'react';
// ThreeJS
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { PCDLoader } from 'three/examples/jsm/loaders/PCDLoader.js';
// Material UI
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
// Socket IO
import io, { Socket } from 'socket.io-client';

let model;
let scene;
let camera;
let renderer;

let frameId;
let verticeCount = 0;

let socket;

const ScanPage: NextPage = () => {

  const mountRef = useRef(null);

  const [isScanning, setIsScanning] = useState(false);

  useEffect(() => {
    console.log("useeffect");

    socket = io("http://localhost:5000");
    socket.on("connect", () => console.log("Socket connected"));
    socket.on("scan/scanning", () => animateScan());
    socket.on("scan/done", () => setIsScanning(false));
    socket.on("disconnect", () => console.log("Socket disconnected"));

    scene = new THREE.Scene();
    scene.background = new THREE.Color( 0x303030 );

    const width = mountRef.current.clientWidth
    const height = mountRef.current.clientHeight

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(width, height);

    // Setup Camera
    camera = new THREE.PerspectiveCamera(
      75, // Field of View
      width / height, // Aspect Ratio
      0.1, // Near clipping
      1000 // Far clipping
    );
    camera.position.z = 2;

    // Camera controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enabled = true;
    controls.enableZoom = false;

    renderer.render(scene, camera);

    let onWindowResize = function () {
      camera.aspect = mountRef.current.clientWidth / mountRef.current.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    }
    window.addEventListener("resize", onWindowResize, false);

    mountRef.current.appendChild(renderer.domElement);

    return () => socket.disconnect()
    // return () => mountRef.current.removeChild(renderer.domElement);
  }, [])

  let scan = (e, path) => {
    setIsScanning(true);
    e.preventDefault();

    if (frameId) cancelAnimationFrame(frameId);
    if (model) scene.remove(model);

    renderer.render(scene, camera);

    const loader = new PCDLoader();
    loader.load(path, (mesh) => {
      mesh.material.color = new THREE.Color( 0x0080ff );
      scene.add(mesh);
      model = mesh;
    });

    verticeCount = 0;
    socket.emit("scan")
  }

  let animateScan = () => {
    if (model) {
      model.rotation.y += 0.002;
      model.geometry.setDrawRange(0, verticeCount);
      if (verticeCount < model.geometry.attributes.position.count) {
          verticeCount += Math.floor(model.geometry.attributes.position.count * 0.001);
      }
    }

    renderer.render(scene, camera);
    frameId = requestAnimationFrame(animateScan);
  }

  return (
    <>
      <Box sx={{ mb: 3, display: "flex", alignItems: "center" }}>
        <Typography variant="h4" sx={{ flexGrow: 1 }}>3D Reconstruction</Typography>
        <Button disabled={isScanning} variant="outlined" onClick={(e) => scan(e, '/screw2.pcd')}>Scan</Button>
      </Box>
      <Box ref={mountRef} sx={{ height: "80vh", width: "100%" }} />
    </>
  )
}

export default ScanPage
