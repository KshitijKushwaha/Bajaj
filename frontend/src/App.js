import React, { useState } from 'react';

function App() {
    const [jsonInput, setJsonInput] = useState('');
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (event) => {
      event.preventDefault();
      try {
          let inputData;
          try {
              inputData = JSON.parse(jsonInput);
          } catch (parseError) {
              // If parsing fails, assume it's a direct array input
              inputData = { data: jsonInput.split(',').map(item => item.trim()) };
          }
  
          console.log('Parsed input data:', inputData);
          
          const requestBody = {
              data: Array.isArray(inputData.data) ? inputData.data : [inputData.data],
              file_b64: inputData.file_b64 || undefined  // Use undefined instead of null
          };
  
          console.log('Request body:', JSON.stringify(requestBody));
  
          const res = await fetch('http://0.0.0.0:10000/bfhl', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(requestBody)
          });
  
          console.log('Response status:', res.status);
          
          if (!res.ok) {
              const errorBody = await res.text();
              throw new Error(`HTTP error! status: ${res.status}, body: ${errorBody}`);
          }
  
          const data = await res.json();
          console.log('Received data:', data);
          setResponse(data);
          setError(null);
      } catch (err) {
          console.error('Error details:', err);
          setError(`Error: ${err.message}`);
          setResponse(null);
      }
  };
  
    return (
        <div className="App">
            <h1>Backend JSON Processor</h1>
            <form onSubmit={handleSubmit}>
                <textarea
                    rows="10"
                    cols="50"
                    value={jsonInput}
                    onChange={(e) => setJsonInput(e.target.value)}
                    placeholder='Enter JSON here'
                />
                <br />
                <button type="submit">Submit</button>
            </form>
            {response && (
                <div>
                    <h3>Response:</h3>
                    <pre>{JSON.stringify(response, null, 2)}</pre>
                </div>
            )}
            {error && <div style={{ color: 'red' }}>{error}</div>}
        </div>
    );
}

export default App;
