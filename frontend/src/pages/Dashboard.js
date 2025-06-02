import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [coinVisuals, setCoinVisuals] = useState({});
  const [correlationImg, setCorrelationImg] = useState('');

  useEffect(() => {
    const fetchVisuals = async () => {
      try {
        const res = await axios.get('https://quantum-coin-api.onrender.com/api/visual-data'); // Your FastAPI route
        setCoinVisuals(res.data.coin_visuals);
        setCorrelationImg(res.data.correlation_img);
      } catch (err) {
        console.error('Error fetching dashboard visuals', err);
      }
    };
    fetchVisuals();
  }, []);

  return (
    <div className="container mt-5">
      <h2 className="mb-4 text-center">Forecast Visual Dashboard</h2>

      {Object.keys(coinVisuals).map((coin) => (
        <div key={coin} className="mb-5">
          <h5 className="text-primary">{coin.replace("coin_", "")}</h5>
          <img
            src={'{coinVisuals[coin].trend}'}
            alt={`${coin} trend`}
            className="img-fluid mb-3 shadow-sm"
          />
          <img
            src={'{coinVisuals[coin].summary}'}
            alt={`${coin} summary`}
            className="img-fluid shadow-sm"
          />
        </div>
      ))}

      <div className="text-center mt-5">
        <h5 className="mb-3">Global Correlation Matrix</h5>
        {correlationImg && (
          <img
            src={'{correlationImg}'}
            alt="Correlation Matrix"
            className="img-fluid shadow-lg"
          />
        )}
      </div>
    </div>
  );
}

export default Dashboard;
