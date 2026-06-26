import { useState, useEffect, useRef } from "react";
import "./App.css";
import GraphView from "./GraphView";

// ✅ Improvement 7: Centralise backend URL via env variable
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [drug1, setDrug1] = useState("");
  const [drug2, setDrug2] = useState("");
  const [result, setResult] = useState(null);
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [suggestions1, setSuggestions1] = useState([]);
  const [suggestions2, setSuggestions2] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false); // ✅ Improvement 3
  const [stats, setStats] = useState({
    total_drugs: 0,
    total_interactions: 0,
    ai_model: "",
  });

  // ✅ Improvement 6: Debounce refs to avoid API call on every keystroke
  const debounceRef1 = useRef(null);
  const debounceRef2 = useRef(null);

  // Load history from localStorage on mount
  useEffect(() => {
    const savedHistory =
      JSON.parse(localStorage.getItem("searchHistory")) || [];
    setHistory(savedHistory);
  }, []);

  // Fetch dashboard stats on mount
  useEffect(() => {
    fetch(`${API_URL}/dashboard/stats`)
      .then((res) => res.json())
      .then((data) => setStats(data))
      .catch((err) => console.error("Stats fetch error:", err));
  }, []);

  // Autocomplete search
  const searchDrugs = async (value, setSuggestions) => {
    if (value.length < 2) {
      setSuggestions([]);
      return;
    }
    try {
      const response = await fetch(
        `${API_URL}/drugs/search?search_term=${value}`
      );
      const data = await response.json();
      setSuggestions(data);
    } catch (error) {
      console.error("Autocomplete error:", error);
      setSuggestions([]);
    }
  };

  // ✅ Improvement 6: Debounced handlers (300ms)
  const handleDrug1Change = (e) => {
    const value = e.target.value;
    setDrug1(value);
    clearTimeout(debounceRef1.current);
    debounceRef1.current = setTimeout(() => {
      searchDrugs(value, setSuggestions1);
    }, 300);
  };

  const handleDrug2Change = (e) => {
    const value = e.target.value;
    setDrug2(value);
    clearTimeout(debounceRef2.current);
    debounceRef2.current = setTimeout(() => {
      searchDrugs(value, setSuggestions2);
    }, 300);
  };

  // Save search to localStorage history
  const saveSearch = (d1, d2) => {
    const newSearch = `${d1} + ${d2}`;
    let existingHistory =
      JSON.parse(localStorage.getItem("searchHistory")) || [];
    existingHistory = [
      newSearch,
      ...existingHistory.filter((item) => item !== newSearch),
    ].slice(0, 5);
    localStorage.setItem("searchHistory", JSON.stringify(existingHistory));
    setHistory(existingHistory);
  };

  // Check drug interaction and fetch graph
  const checkInteraction = async (d1 = drug1, d2 = drug2) => {
    // ✅ Improvement 4: Prevent empty search
    if (!d1.trim() || !d2.trim()) {
      alert("Please enter both drug names before checking.");
      return;
    }

    setLoading(true); // ✅ Improvement 3
    setResult(null);
    setGraphData({ nodes: [], edges: [] }); // ✅ Improvement 2: Clear stale graph

    try {
      // Fetch interaction result
      const interactionResponse = await fetch(
        `${API_URL}/interaction?drug1=${d1}&drug2=${d2}`
      );
      const interactionData = await interactionResponse.json();
      setResult(interactionData);

      // ✅ Improvement 1: Only fetch graph when interaction is found
      if (interactionData.interaction_found) {
        const graphResponse = await fetch(
          `${API_URL}/graph?drug1=${d1}&drug2=${d2}`
        );
        const graph = await graphResponse.json();

        // ✅ Improvement 5: Fixed node positions instead of random
        const nodes = graph.nodes.map((node, index) => ({
          id: node.id,
          data: { label: node.label },
          position: {
            x: 100 + index * 250,
            y: 150,
          },
        }));

        const edges = graph.edges.map((edge) => ({
          id: edge.id,
          source: edge.source,
          target: edge.target,
          label: edge.label,
        }));

        setGraphData({ nodes, edges });
      } else {
        // ✅ Improvement 2: Explicitly clear graph when no interaction
        setGraphData({ nodes: [], edges: [] });
      }

      saveSearch(d1, d2);
    } catch (error) {
      console.error("Interaction check error:", error);
      setResult({
        interaction_found: false,
        message: "Failed to connect to backend",
      });
    } finally {
      setLoading(false); // ✅ Improvement 3
    }
  };

  // ✅ Improvement 9: History click fills inputs AND auto-searches
  const handleHistoryClick = (item) => {
    const drugs = item.split(" + ");
    const d1 = drugs[0];
    const d2 = drugs[1];
    setDrug1(d1);
    setDrug2(d2);
    checkInteraction(d1, d2);
  };

  // Helper: severity badge class
  const severityClass = (level) =>
    level === "High"
      ? "badge high"
      : level === "Moderate"
      ? "badge moderate"
      : "badge low";

  return (
    <div className="container">
      <h1>Drug Interaction Checker</h1>

      {/* Dashboard Stats */}
      <div className="dashboard">
        <div className="card">
          <h3>💊 Total Drugs</h3>
          <h2>{stats.total_drugs.toLocaleString()}</h2>
        </div>
        <div className="card">
          <h3>🔗 Interactions</h3>
          <h2>{stats.total_interactions.toLocaleString()}</h2>
        </div>
        <div className="card">
          <h3>🤖 AI Model</h3>
          <h2>{stats.ai_model}</h2>
        </div>
      </div>

      {/* Search Box */}
      <div className="search-box">

        {/* Drug 1 Input */}
        <div className="autocomplete">
          <input
            type="text"
            placeholder="💊 Enter First Drug"
            value={drug1}
            onChange={handleDrug1Change} // ✅ Improvement 6
          />
          {suggestions1.length > 0 && (
            <ul className="suggestions">
              {suggestions1.map((drug, index) => (
                <li
                  key={index}
                  onClick={() => {
                    setDrug1(drug);
                    setSuggestions1([]);
                  }}
                >
                  {drug}
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Drug 2 Input */}
        <div className="autocomplete">
          <input
            type="text"
            placeholder="💊 Enter Second Drug"
            value={drug2}
            onChange={handleDrug2Change} // ✅ Improvement 6
          />
          {suggestions2.length > 0 && (
            <ul className="suggestions">
              {suggestions2.map((drug, index) => (
                <li
                  key={index}
                  onClick={() => {
                    setDrug2(drug);
                    setSuggestions2([]);
                  }}
                >
                  {drug}
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* ✅ Improvement 3: Loading state on button */}
        <button onClick={() => checkInteraction()} disabled={loading}>
          {loading ? "Checking..." : "Check Interaction"}
        </button>
      </div>

      {/* Interaction Result — from database */}
      {result && result.interaction_found && (
        <div className="result">
          <h2>Result</h2>
          <div className="result-card">
            <h3>Interaction Result</h3>
            <p><strong>Drug 1:</strong> {result.drug1}</p>
            <p><strong>Drug 2:</strong> {result.drug2}</p>
            <p>
              <strong>Severity:</strong>
              <span className={severityClass(result.severity)}>
                {result.severity}
              </span>
            </p>
            <p><strong>Risk Score:</strong> {result.risk_score}/100</p>
            <div className="progress-container">
              <div
                className="progress-bar"
                style={{ width: `${result.risk_score}%` }}
              />
            </div>
            <p><strong>Description:</strong></p>
            <p>{result.description}</p>
            {/* ✅ Improvement 8: Show interaction source */}
            <p>
              <strong>Source:</strong>{" "}
              <span className="badge low">Neo4j Database</span>
            </p>
          </div>
        </div>
      )}

      {/* AI Prediction Result — not in database */}
      {result && !result.interaction_found && (
        <div className="result">
          <h2>AI Prediction</h2>
          <div className="result-card">
            <h3>No Interaction Found In Database</h3>
            <p>{result.message}</p>
            {result.ml_prediction && (
              <>
                <p>
                  <strong>Prediction:</strong>
                  <span className={severityClass(result.ml_prediction)}>
                    {result.ml_prediction}
                  </span>
                </p>
                <p><strong>Confidence:</strong> {result.confidence}%</p>
                <div className="progress-container">
                  <div
                    className="progress-bar"
                    style={{ width: `${result.confidence}%` }}
                  />
                </div>
              </>
            )}
            {/* ✅ Improvement 8: Show AI source label */}
            <p>
              <strong>Source:</strong>{" "}
              <span className="badge moderate">AI Prediction</span>
            </p>
          </div>
        </div>
      )}

      {/* Graph Visualization — only shown when interaction_found */}
      {graphData.nodes.length > 0 && (
        <div className="result">
          <h2>Drug Interaction Graph</h2>
          <GraphView nodes={graphData.nodes} edges={graphData.edges} />
        </div>
      )}

      {/* Recent Search History */}
      {history.length > 0 && (
        <div className="history-card">
          <h3>🕒 Recent Searches</h3>
          <ul>
            {history.map((item, index) => (
              // ✅ Improvement 9: Auto-trigger search on history click
              <li key={index} onClick={() => handleHistoryClick(item)}>
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
