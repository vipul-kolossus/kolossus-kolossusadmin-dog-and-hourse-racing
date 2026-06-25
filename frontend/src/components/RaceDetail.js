import React from 'react';

function RaceDetail({ race, onBack, onAddBet }) {
  const isFinished = race.status === 'finished';
  const sortedParticipants = [...(race.participants || [])].sort((a, b) => a.number - b.number);

  return (
    <div className="race-detail">
      <div className="race-detail-header">
        <button className="back-btn" onClick={onBack}>← Back to Races</button>
        <h2 className="race-detail-title">{race.name}</h2>
        <div className="race-detail-meta">
          <span>{race.race_type === 'dog' ? '🐕 Dog Racing' : '🐎 Horse Racing'}</span>
          <span>📍 {race.track}</span>
          <span>📏 {race.distance}</span>
          <span>💰 Prize: ${parseFloat(race.prize_pool).toLocaleString()}</span>
          <span className={`status-badge status-${race.status}`} style={{ marginLeft: 8 }}>
            {race.status === 'live' ? '🔴 LIVE' : race.status === 'upcoming' ? '⏰ Upcoming' : '✅ Finished'}
          </span>
        </div>
      </div>
      <table className="participants-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            {race.race_type === 'horse' && <th>Jockey</th>}
            <th>Trainer</th>
            <th>Form</th>
            <th>Odds</th>
            {isFinished ? <th>Result</th> : <th>Bet</th>}
          </tr>
        </thead>
        <tbody>
          {sortedParticipants.map(p => (
            <tr key={p.id}>
              <td>
                <span className="participant-number">{p.number}</span>
              </td>
              <td>
                <div className="participant-name">{p.name}</div>
                {p.age && <div style={{ fontSize: 11, color: '#9ca3af' }}>Age: {p.age}{p.weight ? ` • ${p.weight}` : ''}</div>}
              </td>
              {race.race_type === 'horse' && (
                <td style={{ fontSize: 13, color: '#374151' }}>{p.jockey || '—'}</td>
              )}
              <td style={{ fontSize: 13, color: '#374151' }}>{p.trainer || '—'}</td>
              <td>
                <span className="form-display">{p.form || '—'}</span>
              </td>
              <td>
                <span className="odds-display">{parseFloat(p.odds).toFixed(2)}</span>
              </td>
              <td>
                {isFinished ? (
                  p.position ? (
                    <span className={`position-badge pos-${p.position}`}>
                      {p.position === 1 ? '🥇' : p.position === 2 ? '🥈' : p.position === 3 ? '🥉' : `#${p.position}`}
                    </span>
                  ) : '—'
                ) : (
                  <button
                    className="bet-btn"
                    onClick={() => onAddBet(p, race)}
                  >
                    + Bet
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default RaceDetail;
