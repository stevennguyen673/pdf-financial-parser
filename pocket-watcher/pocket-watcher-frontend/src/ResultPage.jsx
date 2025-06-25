import React, { useRef, useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import LiquidGlass from 'liquid-glass-react';
import CirclePackingChart from './CirclePackingChart';
import SankeyDiagram from './SankeyDiagram';

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const containerRef = useRef(null);

  const chartUrls = location.state?.chartUrls || {
    chart_url: "/static/pie_chart.png",
    donut_url: "/static/donut.html",
    bar3d_url: "/static/bar3d.html",
    Circlepacking_url: "./cchart.png",
    schart_url: "./schart.png"
  };

  const [circleData, setCircleData] = useState(null);
  const [sankeyData, setSankeyData] = useState(null);
  const [selectedChart, setSelectedChart] = useState(null);
  const [showGoalForm, setShowGoalForm] = useState(false);
  const [income, setIncome] = useState('');
  const [goal, setGoal] = useState('');
  const [goalUrl, setGoalUrl] = useState(null);
  const [totalSpending] = useState(location.state?.totalSpending || 0);

  const handleUpload = () => navigate('/');
  const handleCharts = () => console.log('Charts clicked');
  const handleGoals = () => setShowGoalForm(true);

  useEffect(() => {
    if (location.state?.circle_data_url) {
      fetch(location.state.circle_data_url)
        .then(res => res.json())
        .then(setCircleData);
    }
    if (location.state?.sankey_data_url) {
      fetch(location.state.sankey_data_url)
        .then(res => res.json())
        .then(setSankeyData);
    }
  }, []);

  const chartData = [
    { title: "Pie Chart", type: "img", url: chartUrls.chart_url },
    { title: "Donut Chart", type: "html", url: chartUrls.donut_url },
    { title: "Bar Chart", type: "html", url: chartUrls.bar3d_url },
    { title: "Circle Packing", type: "img", url: chartUrls.Circlepacking_url},
    { title: "Sankey Diagram", type: "img", url: chartUrls.schart_url }
  ];

  return (
    <div
      ref={containerRef}
      style={{
        minHeight: '100vh',
        width: '100vw',
        position: 'relative',
        overflow: 'hidden',
        color: 'white',
        paddingTop: '7rem',
        paddingBottom: '2rem',
        backgroundImage: 'url("/background.jpg")',
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
      }}
    >
      <LiquidGlass
        mouseContainer={containerRef}
        displacementScale={200}
        blurAmount={0.12}
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
          top: '2rem',
          left: '50%',
          transform: 'translateX(-50%)',
          cursor: 'pointer',
          fontWeight: '600',
          fontSize: '1.25rem',
          zIndex: 10,
        }}
      >
        Pocket Watcher
      </LiquidGlass>

      <div>
        {[{ label: 'Charts', onClick: handleCharts, left: '30%' }, { label: 'Upload More', onClick: handleUpload, left: '50%' }, { label: 'Goals', onClick: handleGoals, left: '70%' }].map(({ label, onClick, left }) => (
          <LiquidGlass
            key={label}
            mouseContainer={containerRef}
            displacementScale={200}
            blurAmount={0.12}
            saturation={140}
            elasticity={0.4}
            aberrationIntensity={2}
            cornerRadius={100}
            padding="12px 32px"
            onClick={onClick}
            style={{
              color: 'white',
              textAlign: 'center',
              position: 'absolute',
              top: '10rem',
              left,
              transform: 'translateX(-50%)',
              cursor: 'pointer',
              fontWeight: '600',
              fontSize: '1.25rem',
              zIndex: 10,
            }}
          >
            {label}
          </LiquidGlass>
        ))}
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '1.5rem',
          marginTop: '18rem',
          padding: '0 2rem',
        }}
      >
        {chartData.map(({ title, url, type, component }) => (
          <div
            key={title}
            onClick={() => setSelectedChart({ title, url, type, component })}
            style={{
              background: 'rgba(255, 255, 255, 0.22)',
              border: '1px solid rgba(255, 255, 255, 0.3)',
              borderRadius: '20px',
              padding: '1rem',
              cursor: 'pointer',
              textAlign: 'center',
              boxShadow: '0 0 12px rgba(0,0,0,0.4)',
              transition: 'transform 0.2s ease',
            }}
          >
            <div
              style={{
                height: '180px',
                overflow: 'hidden',
                marginBottom: '0.5rem',
              }}
            >
              {type === 'img' ? (
                <img src={url} alt={title} style={{ width: '100%', borderRadius: '12px' }} />
              ) : type === 'component' ? (
                component
              ) : (
                <iframe src={url} style={{ width: '100%', height: '100%', border: 'none' }} title={title} />
              )}
            </div>
            <strong>{title}</strong>
          </div>
        ))}
      </div>

      {selectedChart && (
        <div
          onClick={() => setSelectedChart(null)}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            backgroundColor: 'rgba(255, 255, 255, 0.7)',
            zIndex: 1000,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backdropFilter: 'blur(4px)',
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              width: '80%',
              height: '70%',
              borderRadius: '20px',
              overflow: 'hidden',
              boxShadow: '0 0 20px rgba(0,0,0,0.6)',
              backgroundColor: '#000',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <h2 style={{ color: 'white', textAlign: 'center', margin: '1rem 0' }}>{selectedChart.title}</h2>
            {selectedChart.type === 'img' ? (
              <img src={selectedChart.url} alt={selectedChart.title} style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
            ) : selectedChart.type === 'component' ? (
              selectedChart.component
            ) : (
              <iframe src={selectedChart.url} style={{ flexGrow: 1, width: '100%', height: '100%', border: 'none', borderRadius: '0 0 20px 20px' }} title={selectedChart.title} />
            )}
          </div>
        </div>
      )}

      {showGoalForm && (
        <div
          onClick={() => setShowGoalForm(false)}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            zIndex: 1000,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backdropFilter: 'blur(6px)',
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              backgroundColor: 'rgba(0, 0, 0, 0.75)',
              padding: '2rem',
              borderRadius: '20px',
              width: '400px',
              boxShadow: '0 0 20px rgba(0,0,0,0.6)',
              color: 'white',
              display: 'flex',
              flexDirection: 'column',
              gap: '1rem',
            }}
          >
            <h2 style={{ textAlign: 'center' }}>Set Your Goals</h2>
            <label>Monthly Income</label>
            <input
              type="number"
              value={income}
              onChange={(e) => setIncome(e.target.value)}
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '10px',
                border: 'none',
                background: 'rgba(255, 255, 255, 0.35)',
                color: 'white',
              }}
            />
            <label>Savings Goal</label>
            <input
              type="number"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              style={{
                width: '100%',
                padding: '0.5rem',
                borderRadius: '10px',
                border: 'none',
                background: 'rgba(255, 255, 255, 0.29)',
                color: 'white',
              }}
            />
            <button
              onClick={async () => {
                const res = await fetch('/generate_goal', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ income, goal, total_spending: totalSpending }),
                });
                const data = await res.json();
                setGoalUrl(data.goal_url);
                setShowGoalForm(false);
                setSelectedChart({ title: 'Your Savings Progress', url: data.goal_url, type: 'html' });
              }}
              style={{
                marginTop: '1rem',
                padding: '0.75rem 1.25rem',
                backgroundColor: 'limegreen',
                color: 'black',
                fontWeight: 'bold',
                border: 'none',
                borderRadius: '10px',
                cursor: 'pointer',
              }}
            >
              Generate Goal Chart
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
