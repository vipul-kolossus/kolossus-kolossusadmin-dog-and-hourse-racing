import React from 'react';

function BetSlip({ bets, onRemove, onUpdateAmount, onUpdateType, onPlace }) {
  const totalStake = bets.reduce((sum, b) => sum + (parseFloat(b.amount) || 0), 0);
  const totalPotential = bets.reduce((sum, b) => {
    const amt = parseFloat(b.amount) || 0;
    return sum + (amt * parseFloat(b.odds));
  }, 0);

  return (
    <div className="bet-slip">
      <div className="bet-slip-title">
        🎰 Bet Slip
        {bets.length > 0 && <span className="bet-count">{bets.length}</span>}
      </div>

      {bets.length === 0 ? (
        <div className="empty-betslip">
          <div className="empty-betslip-icon">🎯</div>
          <div className="empty-betslip-text">Your bet slip is empty</div>
          <div className="empty-betslip-sub">Click "Bet" on any participant to add selections</div>
        </div>
      ) : (
        <>
          {bets.map(bet => (
            <div key={bet.id} className="bet-item">
              <div className="bet-item-header">
                <div>
                  <div className="bet-participant">#{bet.participantNumber} {bet.participantName}</div>
                  <div className="bet-race">{bet.raceName}</div>
                </div>
                <button className="remove-bet" onClick={() => onRemove(bet.id)}>×</button>
              </div>
              <div className="bet-odds">Odds: {parseFloat(bet.odds).toFixed(2)}</div>
              <select
                className="bet-type-select"
                value={bet.betType}
                onChange={e => onUpdateType(bet.id, e.target.value)}
              >
                <option value="win">Win</option>
                <option value="place">Place</option>
                <option value="each_way">Each Way</option>
              </select>
              <div className="bet-amount-row">
                <input
                  type="number"
                  className="bet-amount-input"
                  placeholder="Amount ($)"
                  value={bet.amount}
                  min="1"
                  onChange={e => onUpdateAmount(bet.id, e.target.value)}
                />
              </div>
              <div className="quick-amount-btns" style={{ marginBottom: 8, display: 'flex', gap: 4 }}>
                {[10, 20, 50, 100].map(amt => (
                  <button key={amt} className="quick-btn" onClick={() => onUpdateAmount(bet.id, String(amt))}>
                    ${amt}
                  </button>
                ))}
              </div>
              {bet.amount && parseFloat(bet.amount) > 0 && (
                <div className="potential-win">
                  💰 Potential win: ${(parseFloat(bet.amount) * parseFloat(bet.odds)).toFixed(2)}
                </div>
              )}
              <button className="place-btn" onClick={() => onPlace(bet)}>
                Place Bet
              </button>
            </div>
          ))}

          {bets.length > 1 && (
            <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: 10, padding: 12, marginTop: 8 }}>
              <div style={{ fontSize: 13, color: '#374151', marginBottom: 4 }}>
                <strong>Total Stake:</strong> ${totalStake.toFixed(2)}
              </div>
              <div style={{ fontSize: 13, color: '#059669', fontWeight: 700 }}>
                <strong>Total Potential Win:</strong> ${totalPotential.toFixed(2)}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default BetSlip;
