import React from 'react';

function formatTime(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function getTimeLabel(race) {
  if (race.status === 'live') return '🔴 LIVE NOW';
  if (race.status === 'finished') return '✅ Finished';
  const diff = new Date(race.start_time) - new Date();
  if (diff < 0) return 'Starting...';
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `In ${mins}m`;
  return `In ${Math.floor(mins / 60)}h ${mins % 60}m`;
}

function RaceList({ races, loading, onSelect }) {
  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p style={{ color: '#6b7280' }}>Loading races...</p>
      </div>
    );
  }

  if (!races.length) {
    return (
      <div className="loading">
        <p style={{ color: '#6b7280', fontSize: 16 }}>No races found.</p>
      </div>
    );
  }

  return (
    <div className="race-grid">
      {races.map(race => (
        <div key={race.id} className="race-card" onClick={() => onSelect(race)}>
          <div className="race-card-header">
            <span className="race-type-badge">
              {race.race_type === 'dog' ? '🐕 Dog' : '🐎 Horse'}
            </span>
            <span className={`status-badge status-${race.status}`}>
              {race.status === 'live' ? '🔴 LIVE' : race.status === 'upcoming' ? '⏰ Upcoming' : '✅ Finished'}
            </span>
          </div>
          <div className="race-card-body">
            <h3 className="race-name">{race.name}</h3>
            <div className="race-meta">
              <span className="race-meta-item">📍 {race.track}</span>
              <span className="race-meta-item">📏 {race.distance}</span>
              <span className="race-meta-item">🕐 {formatTime(race.start_time)}</span>
              <span className="race-meta-item">🐾 {race.participant_count} runners</span>
            </div>
            <div style={{ fontSize: 13, fontWeight: 600, color: race.status === 'live' ? '#dc2626' : '#374151' }}>
              {getTimeLabel(race)}
            </div>
          </div>
          <div className="race-card-footer">
            <span className="prize-pool">💰 Prize: ${parseFloat(race.prize_pool).toLocaleString()}</span>
            <button className="view-btn">View Odds →</button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default RaceList;
