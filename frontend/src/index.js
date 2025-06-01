import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import '/src/styles/index.css'; 

const rootElement = document.getElementById('root');

if (!rootElement) {
  console.error("❌ Couldn't find element with id 'root'. Make sure your index.html has <div id='root'></div>");
} else {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}
