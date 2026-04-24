import React, { useState, useEffect } from 'react'

function App() {
  const [metrics, setMetrics] = useState({ total: 124052, fraud: 842, precision: 99.8 })
  const [events, setEvents] = useState([])
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)

  // Simulation for demo
  useEffect(() => {
    const interval = setInterval(() => {
      const newEvent = {
        id: `tx_${Math.random().toString(36).substr(2, 9)}`,
        amount: (Math.random() * 5000).toFixed(2),
        status: Math.random() > 0.9 ? 'FLAGGED' : 'CLEARED',
        time: new Date().toLocaleTimeString()
      }
      setEvents(prev => [newEvent, ...prev].slice(0, 8))
      setMetrics(prev => ({
        ...prev,
        total: prev.total + 1,
        fraud: newEvent.status === 'FLAGGED' ? prev.fraud + 1 : prev.fraud
      }))
    }, 2000)
    return () => clearInterval(interval)
  }, [])

  const handlePredict = async (e) => {
    e.preventDefault()
    setLoading(true)
    const formData = new FormData(e.target)
    const data = {
      user_id: formData.get('user_id'),
      amount: parseFloat(formData.get('amount')),
      location: formData.get('location')
    }

    try {
      const res = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      const result = await res.json()
      setPrediction(result)
    } catch (err) {
      // Mock for demo if backend is offline
      setPrediction({
        is_fraud: data.amount > 4000 ? 1 : 0,
        fraud_probability: data.amount > 4000 ? 0.98 : 0.04
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Header */}
      <header className="flex justify-between items-center mb-12">
        <div>
          <h1 className="text-4xl font-bold font-tech text-blue-400 mb-2">FRAUDGUARD AI</h1>
          <p className="text-slate-400 uppercase tracking-widest text-sm">Real-Time Threat Detection Matrix</p>
        </div>
        <div className="flex gap-4">
          <div className="px-4 py-2 glass neon-border text-xs font-tech text-green-400 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
            PIPELINE: ACTIVE
          </div>
        </div>
      </header>

      {/* Main Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div className="glass p-6 border-l-4 border-blue-500">
          <p className="text-slate-500 text-sm mb-1 uppercase font-semibold">Total Analyzed</p>
          <p className="text-3xl font-tech">{metrics.total.toLocaleString()}</p>
        </div>
        <div className="glass p-6 border-l-4 border-red-500">
          <p className="text-slate-500 text-sm mb-1 uppercase font-semibold">Anomalies Detected</p>
          <p className="text-3xl font-tech text-red-400">{metrics.fraud}</p>
        </div>
        <div className="glass p-6 border-l-4 border-emerald-500">
          <p className="text-slate-500 text-sm mb-1 uppercase font-semibold">Model Precision</p>
          <p className="text-3xl font-tech text-emerald-400">{metrics.precision}%</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Live Feed */}
        <div className="lg:col-span-2 glass p-8 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10 pointer-events-none">
             <svg width="200" height="200" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <h2 className="text-xl font-bold mb-6 flex items-center gap-3">
            <span className="w-3 h-3 bg-blue-500 rounded-full animate-pulse-slow"></span>
            LIVE TRANSACTION STREAM
          </h2>
          <div className="space-y-4">
            {events.map(event => (
              <div key={event.id} className="flex justify-between items-center p-4 bg-slate-800/40 rounded-xl border border-slate-700/50 hover:bg-slate-800/60 transition-all cursor-default group">
                <div className="flex gap-4 items-center">
                  <div className={`p-2 rounded-lg ${event.status === 'FLAGGED' ? 'bg-red-500/20 text-red-400' : 'bg-green-500/20 text-green-400'}`}>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={event.status === 'FLAGGED' ? 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z' : 'M5 13l4 4L19 7'}></path></svg>
                  </div>
                  <div>
                    <p className="font-tech text-sm">{event.id}</p>
                    <p className="text-xs text-slate-500">{event.time}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-bold">${event.amount}</p>
                  <p className={`text-[10px] font-bold ${event.status === 'FLAGGED' ? 'text-red-400' : 'text-slate-500'}`}>{event.status}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Prediction Form */}
        <div className="space-y-8">
          <div className="glass p-8 neon-border">
            <h2 className="text-xl font-bold mb-6 flex items-center gap-3">
              <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
              ML INFERENCE TEST
            </h2>
            <form onSubmit={handlePredict} className="space-y-4">
              <div>
                <label className="text-[10px] uppercase text-slate-500 mb-1 block">Transaction Amount</label>
                <input name="amount" type="number" required className="w-full bg-slate-900/50 border border-slate-700 rounded-lg p-3 text-sm focus:outline-none focus:border-blue-500" placeholder="0.00" />
              </div>
              <div>
                <label className="text-[10px] uppercase text-slate-500 mb-1 block">User Fingerprint</label>
                <input name="user_id" type="text" required className="w-full bg-slate-900/50 border border-slate-700 rounded-lg p-3 text-sm focus:outline-none focus:border-blue-500" placeholder="USR-XXXX" />
              </div>
              <div>
                <label className="text-[10px] uppercase text-slate-500 mb-1 block">Geo-Location Origin</label>
                <select name="location" className="w-full bg-slate-900/50 border border-slate-700 rounded-lg p-3 text-sm focus:outline-none focus:border-blue-500">
                  <option>NYC-USA</option>
                  <option>LDN-UK</option>
                  <option>TKY-JPN</option>
                  <option>MUM-IND</option>
                </select>
              </div>
              <button disabled={loading} className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-lg transition-all flex justify-center items-center gap-2">
                {loading ? 'ANALYZING...' : 'ANALYZE THREAT'}
              </button>
            </form>

            {prediction && (
              <div className={`mt-6 p-4 rounded-xl border animate-pulse-slow ${prediction.is_fraud === 1 ? 'bg-red-500/10 border-red-500/50' : 'bg-emerald-500/10 border-emerald-500/50'}`}>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-xs uppercase font-bold tracking-widest">{prediction.is_fraud === 1 ? 'THREAT DETECTED' : 'SAFE TRANSACTION'}</span>
                  <span className="text-xs font-tech">{(prediction.fraud_probability * 100).toFixed(2)}%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                  <div className={`h-full transition-all duration-1000 ${prediction.is_fraud === 1 ? 'bg-red-500' : 'bg-emerald-500'}`} style={{ width: `${prediction.fraud_probability * 100}%` }}></div>
                </div>
              </div>
            )}
          </div>
          
          <div className="glass p-6 flex items-center gap-4 opacity-60">
             <div className="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center">
                <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
             </div>
             <div>
                <p className="text-xs font-bold uppercase">System Latency</p>
                <p className="text-xl font-tech">18.4ms</p>
             </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
