import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from './components/Header';
import RaceList from './components/RaceList';
import RaceDetail from './components/RaceDetail';
import BetSlip from './components/BetSlip';
import StatsBar from './components/StatsBar';
import './App.css';

const API_BASE = '/api';

function App() {
  const [races, setRaces] = useState([]);
  const [selectedRace, setSelectedRace] = useState(null);
  const [activeTab, setActiveTab] = useState('all');
  const [bets, setBets] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    fetchRaces();
    fetchStats();
    const interval = setInterval(fetchRaces, 30000);
    return () => clearInterval(interval);
  }, [activeTab]);

  const fetchRaces = async () => {
    try {
      const params = {};
      if (activeTab === 'dog') params.type = 'dog';
      else if (activeTab === 'horse') params.type = 'horse';
      const res = await axios.get(`${API_BASE}/races/`, { params });
      setRaces(res.data.results || res.data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API_BASE}/races/stats/`);
      setStats(res.data);
    } catch (err) {}
  };

  const fetchRaceDetail = async (raceId) => {
    try {
      const res = await axios.get(`${API_BASE}/races/${raceId}/`);
      setSelectedRace(res.data);
    } catch (err) {}
  };

  const addToBetSlip = (participant, race) => {
    const existing = bets.find(b => b.participantId === participant.id);
    if (existing) {
      showNotification('Already in bet slip!', 'warning');
      return;
    }
    setBets(prev => [...prev, {
      id: Date.now(),
      participantId: participant.id,
      participantName: participant.name,
      participantNumber: participant.number,
      raceName: race.name,
      raceId: race.id,
      odds: participant.odds,
      amount: '',
      betType: 'win',
    }]);
    showNotification(`${participant.name} added to bet slip!`, 'success');
  };

  const removeBet = (betId) => {
    setBets(prev => prev.filter(b => b.id !== betId));
  };

  const updateBetAmount = (betId, amount) => {
    setBets(prev => prev.map(b => b.id === betId ? { ...b, amount } : b));
  };

  const updateBetType = (betId, betType) => {
    setBets(prev => prev.map(b => b.id === betId ? { ...b, betType } : b));
  };

  const placeBet = async (bet) => {
    if (!bet.amount || parseFloat(bet.amount) <= 0) {
      showNotification('Please enter a valid amount!', 'error');
      return;
    }
    try {
      await axios.post(`${API_BASE}/bets/`, {
        participant: bet.participantId,
        amount: parseFloat(bet.amount),
        bet_type: bet.betType,
        bettor_name: 'Guest',
      });
      setBets(prev => prev.filter(b => b.id !== bet.id));
      showNotification(`Bet placed on ${bet.participantName}!`, 'success');
      fetchStats();
    } catch (err) {
      showNotification(err.response?.data?.error || 'Failed to place bet', 'error');
    }
  };

  const showNotification = (message, type) => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  return (
    <div className="app">
      <Header stats={stats} />
      <StatsBar stats={stats} />
      {notification && (
        <div className={`notification notification-${notification.type}`}>
          {notification.message}
        </div>
      )}
      <div className="main-layout">
        <div className="races-panel">
          <div className="tabs">
            {['all', 'dog', 'horse'].map(tab => (
              <button
                key={tab}
                className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
                onClick={() => { setActiveTab(tab); setSelectedRace(null); }}
              >
                {tab === 'all' ? '🏁 All Races' : tab === 'dog' ? '🐕 Dog Racing' : '🐎 Horse Racing'}
              </button>
            ))}
          </div>
          {selectedRace ? (
            <RaceDetail
              race={selectedRace}
              onBack={() => setSelectedRace(null)}
              onAddBet={addToBetSlip}
            />
          ) : (
            <RaceList
              races={races}
              loading={loading}
              onSelect={(race) => fetchRaceDetail(race.id)}
            />
          )}
        </div>
        <div className="betslip-panel">
          <BetSlip
            bets={bets}
            onRemove={removeBet}
            onUpdateAmount={updateBetAmount}
            onUpdateType={updateBetType}
            onPlace={placeBet}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
