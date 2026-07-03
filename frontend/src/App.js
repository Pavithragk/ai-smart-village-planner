import React, { useState } from 'react';
import axios from 'axios';
import jsPDF from 'jspdf';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';

const API = 'http://localhost:8000';

function App() {
  const [form, setForm] = useState({
    name: '', district: '', state: 'Karnataka',
    population: '', area_hectares: '', rainfall_mm: '',
    water_sources: '', num_schools: '', num_health_centers: '',
    primary_crops: '', soil_type: 'loamy', budget_lakhs: '',
    electricity: true, road_connectivity: true,
    latitude: '12.9716', longitude: '77.5946'
  });
  const [village, setVillage] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState('form');

  const handleChange = e => {
    const { name, value, type, checked } = e.target;
    setForm(f => ({ ...f, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    try {
      const { latitude, longitude, ...rest } = form;
      const payload = {
        ...rest,
        population: parseInt(form.population),
        area_hectares: parseFloat(form.area_hectares),
        rainfall_mm: parseFloat(form.rainfall_mm),
        water_sources: parseInt(form.water_sources),
        num_schools: parseInt(form.num_schools),
        num_health_centers: parseInt(form.num_health_centers),
        budget_lakhs: parseFloat(form.budget_lakhs),
      };
      const res = await axios.post(`${API}/api/villages/`, payload);
      setVillage({ ...res.data, latitude: parseFloat(form.latitude), longitude: parseFloat(form.longitude) });
      setStep('loading');
      const id = res.data.id;
      const modules = ['agriculture', 'water', 'healthcare', 'education', 'schemes'];
      const allResults = [];
      for (let mod of modules) {
        const r = await axios.post(`${API}/api/${mod}/${id}`);
        allResults.push(r.data);
        setResults([...allResults]);
      }
      setStep('results');
    } catch (err) {
      alert('Error: ' + err.message);
    }
    setLoading(false);
  };

  const priorityColor = p => p === 'critical' ? '#dc2626' : p === 'high' ? '#ea580c' : '#16a34a';
  const totalBudget = results.reduce((sum, r) => sum + (r.cost_lakhs || 0), 0);

  const downloadPDF = () => {
    const doc = new jsPDF();
    let y = 20;
    const pageHeight = 280;
    const margin = 15;
    const maxWidth = 180;
    doc.setFontSize(18);
    doc.setTextColor(22, 101, 52);
    doc.text(`${village.name} - Development Report`, margin, y);
    y += 8;
    doc.setFontSize(11);
    doc.setTextColor(80, 80, 80);
    doc.text(`${village.district}, ${village.state} | Population: ${village.population}`, margin, y);
    y += 6;
    doc.text(`Total Estimated Budget: Rs.${totalBudget.toFixed(1)} Lakhs`, margin, y);
    y += 10;
    results.forEach(r => {
      if (y > pageHeight - 20) { doc.addPage(); y = 20; }
      doc.setFontSize(13);
      doc.setTextColor(22, 101, 52);
      doc.text(`${r.title} [${r.priority?.toUpperCase()}]`, margin, y);
      y += 7;
      doc.setFontSize(9);
      doc.setTextColor(40, 40, 40);
      const lines = doc.splitTextToSize(r.content, maxWidth);
      lines.forEach(line => {
        if (y > pageHeight) { doc.addPage(); y = 20; }
        doc.text(line, margin, y);
        y += 4.5;
      });
      y += 5;
      doc.setTextColor(100, 100, 100);
      doc.text(`Estimated Cost: Rs.${r.cost_lakhs} Lakhs`, margin, y);
      y += 10;
    });
    doc.save(`${village.name}_Development_Report.pdf`);
  };

  if (step === 'results') return (
    <div style={{ fontFamily: 'Arial', maxWidth: 900, margin: '0 auto', padding: 20 }}>
      <div style={{ background: '#166534', color: 'white', padding: 20, borderRadius: 10, marginBottom: 15 }}>
        <h1 style={{ margin: 0 }}> {village.name} — Development Report</h1>
        <p style={{ margin: '5px 0 0' }}>{village.district}, {village.state} | Population: {village.population}</p>
      </div>
      <div style={{ height: '300px', width: '100%', borderRadius: 10, overflow: 'hidden', marginBottom: 20, border: '1px solid #e5e7eb' }}>
        <MapContainer center={[village.latitude, village.longitude]} zoom={13} style={{ height: '300px', width: '100%' }} scrollWheelZoom={false}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='&copy; OpenStreetMap contributors' />
          <Marker position={[village.latitude, village.longitude]}>
            <Popup>{village.name}<br />Population: {village.population}</Popup>
          </Marker>
        </MapContainer>
      </div>
      <div style={{ background: '#fef3c7', border: '1px solid #f59e0b', borderRadius: 10, padding: 15, marginBottom: 20, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <strong style={{ fontSize: 18, color: '#92400e' }}>Total Estimated Budget: Rs.{totalBudget.toFixed(1)} Lakhs</strong>
          <p style={{ margin: '5px 0 0', color: '#92400e', fontSize: 13 }}>Across {results.length} development areas</p>
        </div>
        <button onClick={downloadPDF} style={{ background: '#166534', color: 'white', border: 'none', padding: '10px 20px', borderRadius: 8, fontSize: 14, cursor: 'pointer', fontWeight: 600 }}>
          Download PDF Report
        </button>
      </div>
      {results.map((r, i) => (
        <div key={i} style={{ background: 'white', border: '1px solid #e5e7eb', borderRadius: 10, padding: 20, marginBottom: 15, borderLeft: `5px solid ${priorityColor(r.priority)}` }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
            <h2 style={{ margin: 0, color: '#1f2937' }}>{r.title}</h2>
            <span style={{ background: priorityColor(r.priority), color: 'white', padding: '3px 10px', borderRadius: 20, fontSize: 13 }}>{r.priority?.toUpperCase()}</span>
          </div>
          <pre style={{ background: '#f9fafb', padding: 15, borderRadius: 8, fontSize: 13, lineHeight: 1.6, whiteSpace: 'pre-wrap', margin: 0 }}>{r.content}</pre>
          <p style={{ color: '#6b7280', margin: '10px 0 0' }}>💰 Estimated Cost: Rs.{r.cost_lakhs} Lakhs</p>
        </div>
      ))}
      <div style={{ display: 'flex', gap: 10 }}>
        <button onClick={downloadPDF} style={{ background: '#166534', color: 'white', border: 'none', padding: '12px 30px', borderRadius: 8, fontSize: 16, cursor: 'pointer' }}>
          Download PDF Report
        </button>
        <button onClick={() => { setStep('form'); setResults([]); setVillage(null); }} style={{ background: 'white', color: '#166534', border: '2px solid #166534', padding: '12px 30px', borderRadius: 8, fontSize: 16, cursor: 'pointer' }}>
          + Analyze Another Village
        </button>
      </div>
    </div>
  );

  if (step === 'loading') return (
    <div style={{ fontFamily: 'Arial', textAlign: 'center', padding: 60 }}>
      <h2 style={{ color: '#166534' }}>AI is analyzing {form.name}...</h2>
      {results.map((r, i) => <p key={i} style={{ color: '#16a34a' }}>✅ {r.title} ready</p>)}
      <p style={{ color: '#6b7280' }}>Please wait...</p>
    </div>
  );

  return (
    <div style={{ fontFamily: 'Arial', maxWidth: 800, margin: '0 auto', padding: 20 }}>
      <div style={{ background: '#166534', color: 'white', padding: 25, borderRadius: 10, marginBottom: 25, textAlign: 'center' }}>
        <h1 style={{ margin: 0 }}> AI Smart Village Development Planner</h1>
        <p style={{ margin: '8px 0 0', opacity: 0.9 }}>Enter village details to get AI-powered development recommendations</p>
      </div>
      <form onSubmit={handleSubmit} style={{ background: 'white', padding: 25, borderRadius: 10, border: '1px solid #e5e7eb' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 15 }}>
          {[
            ['name', 'Village Name *', 'text', 'e.g. Hosakote'],
            ['district', 'District *', 'text', 'e.g. Bengaluru Rural'],
            ['population', 'Population *', 'number', 'e.g. 4500'],
            ['area_hectares', 'Area (Hectares) *', 'number', 'e.g. 320'],
            ['rainfall_mm', 'Annual Rainfall (mm) *', 'number', 'e.g. 680'],
            ['water_sources', 'Water Sources (count)', 'number', 'e.g. 2'],
            ['num_schools', 'Number of Schools', 'number', 'e.g. 3'],
            ['num_health_centers', 'Health Centers', 'number', 'e.g. 1'],
            ['primary_crops', 'Primary Crops', 'text', 'e.g. rice, ragi'],
            ['budget_lakhs', 'Budget (Lakhs Rs.) *', 'number', 'e.g. 150'],
            ['latitude', 'Latitude (map location)', 'text', 'e.g. 12.9716'],
            ['longitude', 'Longitude (map location)', 'text', 'e.g. 77.5946'],
          ].map(([name, label, type, placeholder]) => (
            <div key={name}>
              <label style={{ display: 'block', marginBottom: 5, color: '#374151', fontWeight: 500 }}>{label}</label>
              <input name={name} type={type} placeholder={placeholder} value={form[name]} onChange={handleChange}
                style={{ width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: 6, fontSize: 14, boxSizing: 'border-box' }} required={label.includes('*')} />
            </div>
          ))}
          <div>
            <label style={{ display: 'block', marginBottom: 5, color: '#374151', fontWeight: 500 }}>State</label>
            <select name="state" value={form.state} onChange={handleChange} style={{ width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: 6, fontSize: 14 }}>
              {['Karnataka', 'Tamil Nadu', 'Andhra Pradesh', 'Telangana', 'Maharashtra', 'Kerala'].map(s => <option key={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: 5, color: '#374151', fontWeight: 500 }}>Soil Type</label>
            <select name="soil_type" value={form.soil_type} onChange={handleChange} style={{ width: '100%', padding: '10px', border: '1px solid #d1d5db', borderRadius: 6, fontSize: 14 }}>
              {['loamy', 'sandy', 'clayey', 'black', 'red'].map(s => <option key={s}>{s}</option>)}
            </select>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 20, margin: '15px 0' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer' }}>
            <input type="checkbox" name="electricity" checked={form.electricity} onChange={handleChange} /> Electricity Available
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer' }}>
            <input type="checkbox" name="road_connectivity" checked={form.road_connectivity} onChange={handleChange} /> Road Connectivity
          </label>
        </div>
        <button type="submit" disabled={loading} style={{ width: '100%', background: '#166534', color: 'white', border: 'none', padding: '14px', borderRadius: 8, fontSize: 16, cursor: 'pointer', fontWeight: 600 }}>
          {loading ? 'Analyzing...' : ' Generate AI Development Plan'}
        </button>
      </form>
    </div>
  );
}

export default App;