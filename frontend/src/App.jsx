import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Teams from './pages/Teams'
import './App.css'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/teams" element={<Teams />} />
    </Routes>
  )
}

export default App