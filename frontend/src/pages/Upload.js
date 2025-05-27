import React, { useState } from 'react';
import axios from 'axios';

function Upload() {
  const [file, setFile] = useState(null);
  const [coin, setCoin] = useState('');
  const [year, setYear] = useState('2030');
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file || !coin) {
      alert('Please fill all fields and upload a CSV file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('coin', coin);
    formData.append('target_year', year);

    try {
      const res = await axios.post('/upload_predict', formData);
      setResult(res.data);
    } catch (err) {
      console.error('Upload failed', err);
      alert('Prediction failed. Check your file format.');
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4 text-center">Upload Your Own Data</h2>

      <div className="mb-3">
        <label className="form-label">Coin Name</label>
        <input
          type="text"
          className="form-control"
          placeholder="e.g. coin_CustomCoin"
          value={coin}
          onChange={(e) => setCoin(e.target.value)}
        />
      </div>

      <div className="mb-3">
        <label className="form-label">Target Year</label>
        <select
          className="form-select"
          value={year}
          onChange={(e) => setYear(e.target.value)}
        >
          {[2026, 2030, 2040, 2050].map((y) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-3">
        <label className="form-label">Upload CSV File</label>
        <input
          type="file"
          className="form-control"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </div>

      <button className="btn btn-primary" onClick={handleUpload}>
        Upload and Forecast
      </button>

      {result && (
        <>
          <div className="text-center mt-4">
            <img
              src={`data:image/png;base64,${result.chart}`}
              alt="Forecast Chart"
              className="img-fluid shadow-sm"
            />
          </div>

          <div className="table-responsive mt-4">
            <table className="table table-striped">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Predicted Price</th>
                </tr>
              </thead>
              <tbody>
                {result.forecast.map((row, idx) => (
                  <tr key={idx}>
                    <td>{row.ds}</td>
                    <td>${parseFloat(row.yhat).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}

export default Upload;
