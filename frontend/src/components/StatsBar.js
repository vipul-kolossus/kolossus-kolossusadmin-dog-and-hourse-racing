import React from 'react';

function StatsBar({ stats }) {
  return (
    <div className="stats-bar">
      <div className="stat-item">
        <span className="stat-icon">🏁</span>
        <div className="stat-info">
          <span className="stat-value">{stats.total_races || 0}</span>
          <span className="stat-label">Total Races</span>
        </div>
      </div>
      <div className="stat-item">
        <span className="stat-icon">🔴</span>
        <div className="stat-info">
          <span className="stat-value">{stats.live_races || 0}</span>
          <span className="stat-label">Live Now</span>
        </div>
      </div>
      <div className="stat-item">
        <span className="stat-icon">🐕</span>
        <div className="stat-info">
          <span className="stat-value">{stats.dog_races || 0}</span>
          <span className="stat-label">Dog Races</span>
        </div>
      </div>
      <div className="stat-item">
        <span className="stat-icon">🐎</span>
        <div className="stat-info">
          <span className="stat-value">{stats.horse_races || 0}</span>
          <span className="stat-label">Horse Races</span>
        </div>
      </div>
      <div className="stat-item">
        <span className="stat-icon">🎯</span>
        <div className="stat-info">
          <span className="stat-value">{stats.total_bets || 0}</span>
          <span className="stat-label">Bets Placed</span>
        </div>
      </div>
      <div className="stat-item">
        <span className="stat-icon">💰</span>
        <div className="stat-info">
          <span className="stat-value">${(stats.total_wagered || 0).toFixed(0)}</span>
          <span className="stat-label">Total Wagered</span>
        </div>
      </div>
    </div>
  );
}

export default StatsBar;
