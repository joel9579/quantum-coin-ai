import React, { useState } from 'react';
import axios from 'axios';

function PredictionPage() {
  const [coin, setCoin] = useState("coin_Bitcoin");
  const [year, setYear] = useState("2030");
  const [forecast, setForecast] = useState([]);
  const [chart, setChart] = useState("");

  const handlePredict = async () => {
    try {
      const res = await axios.post("/predict", {
        coin: coin,
        target_year: parseInt(year)
      });
      setForecast(res.data.forecast);
      setChart(res.data.chart);
    } catch (err) {
      alert("Prediction failed!");
    }
  };

useEffect(() => {
  const fetchCoins = async () => {
    const res = await axios.get("/coins");
    setCoinList(res.data.coins); // save to local state
  };
  fetchCoins();
}, []);

<select value={coin} onChange={(e) => setCoin(e.target.value)}>
  {coinList.map(c => (
    <option key={c} value={c}>{c.replace('coin_', '')}</option>
  ))}
</select>

  return (
    <div className="container">
      <h2 className="my-4">Generate Forecast</h2>
      <div className="mb-3">
        <label>Coin:</label>
        <select className="form-select" value={coin} onChange={(e) => setCoin(e.target.value)}>
          <option value="coin_Bitcoin">Bitcoin</option>
          <option value="coin_Ethereum">Ethereum</option>
          <option value="coin_Solana">Solana</option>
          <option value="coin_Cardano">Cardano</option>
        </select>
      </div>
      <div className="mb-3">
        <label>Target Year:</label>
        <select className="form-select" value={year} onChange={(e) => setYear(e.target.value)}>
          <option value="2026">2026</option>
          <option value="2030">2030</option>
          <option value="2040">2040</option>
          <option value="2050">2050</option>
        </select>
      </div>
      <button className="btn btn-primary" onClick={handlePredict}>Generate Forecast</button>

      {chart && (
        <div className="mt-5 text-center">
          <img src={`data:image/png;base64,${chart}`} alt="Forecast Chart" className="img-fluid" />
        </div>
      )}

      {forecast.length > 0 && (
        <div className="mt-4">
          <h4>Forecast Table</h4>
          <table className="table table-striped">
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

export default PredictionPage;
