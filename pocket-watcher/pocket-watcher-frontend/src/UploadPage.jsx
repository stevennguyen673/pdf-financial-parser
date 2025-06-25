import React, { useRef, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import LiquidGlass from 'liquid-glass-react';

export default function UploadPage() {
  const containerRef = useRef(null);
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const navigate = useNavigate();

  const onDrop = (acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setUploadStatus('');
    }
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: '.pdf,.csv,.xlsx,.json',
    maxFiles: 1,
  });

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploadStatus('Uploading...');
      const res = await axios.post('http://localhost:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      console.log('Response:', res.data);
      setUploadStatus('Upload successful!');
      navigate('/results', {
        state: {
          chartUrl: `http://localhost:5000${res.data.chart_url}`,
        },
      });
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('Upload failed. Please try again.');
    }
  };

  return (
    <div
      ref={containerRef}
      style={{
        width: '100vw',
        height: '100vh',
        position: 'relative',
        overflow: 'hidden',
        backgroundImage: 'url("/background.jpg")',
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat'
      }}
    >

      {/* Glass */}
      <LiquidGlass
        mouseContainer={containerRef}
        displacementScale={200}
        blurAmount={0.3}
        saturation={140}
        elasticity={0.2}
        aberrationIntensity={2}
        cornerRadius={32}
        glassSize = {{ width: 700, height: 150 }}
        
        style={{
          position: 'absolute',
          top: '45%',
          left: '50%',
          textAlign: 'center',
          color: 'white',
        }}
      >
        <h2 style={{ marginBottom: '1rem', fontSize: '1.3rem' }}>
          Transform Your Financial Snapshot
        </h2>
        <div
          {...getRootProps()}
          style={{
            border: '2px dashed white',
            borderRadius: '16px',
            padding: '10px',
            cursor: 'pointer',
            transition: 'border-color 0.2s ease',
          }}
        >
          <input {...getInputProps()} />
          <p>{file ? `Selected File: ${file.name}` : 'Drop a file or tap to select'}</p>
        </div>
        <p style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#ccc' }}>
          {uploadStatus}
        </p>
      </LiquidGlass>

      {/* Button */}
      <LiquidGlass
        mouseContainer={containerRef}
        displacementScale={200}
        blurAmount={0.10}
        saturation={140}
        elasticity={0.4}
        aberrationIntensity={2}
        cornerRadius={100}
        padding="12px 32px"
        onClick={handleUpload}
        style={{
          color: 'white',
          textAlign: 'center',
          position: 'absolute',
          top: '75%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          cursor: 'pointer',
          fontWeight: '600',
          fontSize: '1rem',
        }}
      >
        Continue
      </LiquidGlass>
    </div>
  );
}
