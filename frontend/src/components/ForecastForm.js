import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ForecastForm() {
  const [coins, setCoins] = useState([]);
  const [years, setYears] = useState([]);
  const [selectedCoin, setSelectedCoin] = useState('');
  const [selectedYear, setSelectedYear] = useState('2030');

  useEffect(() => {
    // Fetch coins
    axios.get('https://quantum-coin-api.onrender.com/api/coins')
      .then(res => {
        setCoins(res.data.coins);
        setSelectedCoin(res.data.coins[0]); // Set default
      })
      .catch(err => console.error("Error fetching coins", err));

    // Fetch years
    axios.get('https://quantum-coin-api.onrender.com/api/years')
      .then(res => setYears(res.data.years))
      .catch(err => console.error("Error fetching years", err));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    window.location.href = `/result?coin=${selectedCoin}&target_year=${selectedYear}`;
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 max-w-md mx-auto">
      <div>
        <label htmlFor="coin" className="block font-medium mb-1">Select Coin</label>
        <select
          name="coin"
          id="coin"
          value={selectedCoin}
          onChange={(e) => setSelectedCoin(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2"
        >
          {coins.map((c, index) => (
            <option key={index} value={c}>{c.replace("coin_", "")}</option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="target_year" className="block font-medium mb-1">Forecast up to Year</label>
        <select
          name="target_year"
          id="target_year"
          value={selectedYear}
          onChange={(e) => setSelectedYear(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2"
        >
          {years.map((y, index) => (
            <option key={index} value={y}>{y}</option>
          ))}
        </select>
      </div>

      <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
        Forecast
      </button>
    </form>
  );
}

export default ForecastForm;
