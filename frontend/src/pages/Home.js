import React from 'react';
import { Link } from 'react-router-dom';
import btc from '../assets/btc.png';
import eth from '../assets/eth.png';
import sol from '../assets/sol.png';
import ada from '../assets/ada.png';

function Home() {
  const trendingCoins = [
    { name: 'Bitcoin', icon: btc },
    { name: 'Ethereum', icon: eth },
    { name: 'Solana', icon: sol },
    { name: 'Cardano', icon: ada }
  ];

  return (
    <div className="container text-center mt-4">
      <h1 className="fw-bold text-dark mb-2">Welcome to <span className="text-primary">Quantum Coin AI</span></h1>
      <p className="text-muted mb-5">
        Predict future cryptocurrency prices up to 10–30 years using global deep learning models.
      </p>

      <h4 className="mb-3">Trending Coins</h4>
      <div className="d-flex justify-content-center gap-4 flex-wrap mb-5">
        {trendingCoins.map((coin) => (
          <div key={coin.name} className="text-center">
            <img src={coin.icon} alt={coin.name} width={60} className="mb-2" />
            <div className="fw-semibold">{coin.name}</div>
          </div>
        ))}
      </div>

      <h4 className="mb-3">Start Forecasting</h4>
      <div className="d-flex justify-content-center gap-3">
        <Link to="/predict" className="btn btn-primary">Prediction</Link>
        <Link to="/dashboard" className="btn btn-outline-info">Visual Dashboard</Link>
        <Link to="/upload" className="btn btn-success">Upload CSV</Link>
      </div>
    </div>
  );
}

export default Home;
