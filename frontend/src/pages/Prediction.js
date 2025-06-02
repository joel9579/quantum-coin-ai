import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Prediction() {
  const [coinList, setCoinList] = useState([]);
  const [coin, setCoin] = useState('');
  const [year, setYear] = useState('2030');
  const [forecast, setForecast] = useState([]);
  const [chart, setChart] = useState('');

  useEffect(() => {
    const fetchCoins = async () => {
      try {
        const res = await axios.get('https://quantum-coin-api.onrender.com/api/coins');
        setCoinList(res.data.coins);
        setCoin(res.data.coins[0]);
      } catch (err) {
        console.error('Failed to load coins', err);
      }
    };
    fetchCoins();
  }, []);

  const handlePredict = async () => {
    try {
      const res = await axios.post('https://quantum-coin-api.onrender.com/api/predict', fromData) {
        coin: coin,
        target_year: parseInt(year)
      });
      setForecast(res.data.forecast);
      setChart(res.data.chart);
    } catch (err) {
      console.error('Prediction error', err);
      alert('Prediction failed. Please try again.');
    }
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4 text-center">Cryptocurrency Forecast</h2>

      <div className="row mb-4">
        <div className="col-md-5">
          <label className="form-label fw-semibold">Select Coin</label>
          <select className="form-select" value={coin} onChange={(e) => setCoin(e.target.value)}>
            {coinList.map((c, i) => (
              <option key={i} value={c}>{c.replace("coin_", "")}</option>
            ))}
          </select>
        </div>

        <div className="col-md-4">
          <label className="form-label fw-semibold">Forecast Year</label>
          <select className="form-select" value={year} onChange={(e) => setYear(e.target.value)}>
            {[2026, 2030, 2040, 2050].map((y) => (
              <option key={y} value={y}>{y}</option>
            ))}
          </select>
        </div>

        <div className="col-md-3 d-flex align-items-end">
          <button className="btn btn-primary w-100" onClick={handlePredict}>Generate Forecast</button>
        </div>
      </div>

      {chart && (
        <div className="text-center mb-4">
          <img src={`data:image/png;base64,${chart}`} alt="Forecast Chart" className="img-fluid shadow-sm" />
        </div>
      )}

      {forecast.length > 0 && (
        <div className="table-responsive">
          <table className="table table-striped table-bordered">
            <thead>
              <tr>
                <th>Date</th>
                <th>Predicted Price (USD)</th>
              </tr>
            </thead>
            <tbody>
              {forecast.map((row, idx) => (
                <tr key={idx}>
                  <td>{row.ds}</td>
                  <td>${parseFloat(row.yhat).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Prediction;
