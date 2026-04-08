import React, { useEffect, useState } from 'react';
import { fetchHistory } from '../api';
import { Clock, History } from 'lucide-react';

export default function HistorySidebar({ onSelectRecipe }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchHistory();
        setHistory(data);
      } catch (err) {
        console.error("Failed to load history", err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return <div className="history-sidebar panel skeleton">Loading history...</div>;
  }

  return (
    <div className="history-sidebar panel slide-in-left">
      <div className="history-header">
        <h3><History size={18}/> Recent Recipes</h3>
      </div>
      {history.length === 0 ? (
        <p className="empty-text">No recipes generated yet.</p>
      ) : (
        <ul className="history-list">
          {history.map((rec) => (
            <li key={rec.id} onClick={() => onSelectRecipe(rec)} className="history-item">
              <h4>{rec.name}</h4>
              <span className="time"><Clock size={12}/> {rec.cook_time}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
