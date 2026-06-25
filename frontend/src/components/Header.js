import React from 'react';

function Header({ stats }) {
  return (
    <header className="header">
      <div className="header-brand">
        <span className="header-logo">🏆</span>
        <h1 className="header-title">EdgeBet <span>Pro</span></h1>
        {stats.live_races > 0 && (
          <span className="header-badge">🔴 {stats.live_races} Live</span>
        )}
      </div>
      <div className="header-stats">
        <div className="header-stat">
          <div className="header-stat-value">{stats.total_races || 0}</div>
          <div className="header-stat-label">Total Races</div>
        </div>
        <div className="header-stat">
          <div className="header-stat-value">{stats.total_bets || 0}</div>
          <div className="header-stat-label">Total Bets</div>
        </div>
        <div className="header-stat">
          <div className="header-stat-value">${(stats.total_wagered || 0).toLocaleString()}</div>
          <div className="header-stat-label">Total Wagered</div>
        </div>
      </div>
    </header>
  );
}

export default Header;
