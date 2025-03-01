import './App.css'
import { useState, useEffect } from 'react'

function App() {

  const [industry, setIndustry] = useState("")
  const [topics, setTopics] = useState([])
  const [topic, setTopic] = useState("")
  const [model, setModel] = useState("gpt-4o-2024-08-06")
  const [threshold, setThreshold] = useState(0.85)
  const [apiKey, setApiKey] = useState("")
  const [error, setError] = useState("")
  const [formSubmitted, setFormSubmitted] = useState(false)
  const [status, setStatus] = useState("");
  const baseAPIUrl = "http://localhost:8000"
  

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/status");
    ws.onmessage = (event) => {
        setStatus(event.data);
    };
    return () => ws.close();
  }, []);


  const numbers = Array.from(
    { length: ((1.0 - 0.05) / 0.05) + 1 },
    (_, i) => Number((0.05 + (i * 0.05)).toFixed(2))
  )

  const handleAddTopic = (topic, e) => {
    if (error) {
      setError("")
    }
    e.preventDefault()
    if (topic.trim() !== "" && !topics.includes(topic)) {
      setTopics([...topics, topic])
      setTopic("")
    } else {
      setError("Topic already exists")
    }
  }

  const handleRemoveTopic = (topic, e) => {
    e.preventDefault()
    setTopics(topics.filter((t) => t !== topic))
  }


  const handleSubmitForm = async (e) => {
    e.preventDefault()
    setFormSubmitted(true)
    try {
      const response = await fetch(`${baseAPIUrl}/generate-report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          industry,
          topics,
          model,
          threshold,
          api_key: apiKey,
        }),
      })
      const data = await response.json()
      console.log(data)
    } catch (error) {
      console.error("Error in report generation:", error)
    }
  }

  

  return (
    <div className="general-container">
      <h1>Industry Report Generator</h1>
      <div className="app-container">
        <form>
          <label>
            <span>Industry Name</span>
            <input 
              type="text" 
              value={industry} 
              onChange={(e) => setIndustry(e.target.value)}
              placeholder="e.g. Healthcare, Technology, Finance"
            />
          </label>
          <label>
            <span>Topics</span>
            <div className="topics-container">
              <input 
                type="text" 
                value={topic} 
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Enter topic"
              />
              <button className="add-topic-button" onClick={(e) => handleAddTopic(topic, e)}>Add</button>
            </div>
            <div className="topics-list">
              {topics.map((topic, index) => (
                <span className="single-topic" key={index}>
                  {topic}
                  <button 
                    className="remove-topic" 
                    onClick={(e) => handleRemoveTopic(topic, e)}
                    style={{ outline: 'none' }}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M18 6L6 18M6 6l12 12"/>
                    </svg>
                  </button>
                </span>

                ))}
            </div>
            {error && <p className="error">{error}</p>}
          </label>
          <label>
            <span>Model</span>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
            >
              <option value="gpt-4o-2024-08-06">GPT-4o</option>
              <option value="gpt-4o-mini-2024-07-18">GPT-4o-mini</option>
              <option value="o3-mini-2025-01-31">GPT-o3-mini</option>
              <option value="gpt-4-turbo-2024-04-09">GPT-4-turbo</option>
            </select>
          </label>
          <label>
            <span>Confidence Threshold</span>
            <select
              value={threshold}
              onChange={(e) => setThreshold(parseFloat(e.target.value))}
            >
              {numbers.map((number) => (
                <option value={number}>{number}</option>
              ))}
            </select>
          </label>
          <label>
            <span>OpenAI API Key</span>
            <input 
              type="password" 
              value={apiKey} 
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-..."
            />
          </label>
          <button className="generate-report-button" onClick={(e) => handleSubmitForm(e)} type="submit">Generate Report</button>
        </form>  
        {formSubmitted && (
          <div className="report-container">
            <h3>Report Generation Status</h3>
            <div className="status-message">
              {status || "Initializing..."}
            </div>
            {error && <div className="error-message">{error}</div>}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
