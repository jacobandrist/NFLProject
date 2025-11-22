import { Link } from 'react-router-dom'
import { useEffect, useRef } from 'react'

function Home() {
  const observerRef = useRef(null)

  useEffect(() => {
    const counters = document.querySelectorAll('.stat-number')
    const speed = 100

    const animateCounters = () => {
      counters.forEach(counter => {
        const target = +counter.getAttribute('data-target')
        let count = 0
        
        const updateCount = () => {
          const increment = target / speed
          
          if (count < target) {
            count += increment
            counter.innerText = Math.ceil(count)
            requestAnimationFrame(updateCount)
          } else {
            counter.innerText = target
          }
        }
        
        updateCount()
      })
    }

    const observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        animateCounters()
      }
    }, { threshold: 0.3 })

    const leadersSection = document.querySelector('#leaders')
    if (leadersSection) {
      observer.observe(leadersSection)
    }

    return () => {
      if (leadersSection) {
        observer.unobserve(leadersSection)
      }
    }
  }, [])

  return (
    <>
      <nav>
        <div className="nav-left">
          <img src="https://cdn.freebiesupply.com/logos/large/2x/nfl-logo.png" alt="NFL Logo" className="Nav-logo"/>
          <h3>NFL Stats Hub</h3>
        </div>
        <div className="links">
          <Link to="/">Home</Link>
          <Link to="/teams">Teams</Link>
          <a href="#predictions">Predictions</a>
        </div>
      </nav>

      <section className="hero">
        <h1>Track Performance. Forecast Greatness.</h1>
        <p>All the stats you need.</p>
      </section>

      <section className="section" id="leaders">
        <h2>Season Stat Leaders</h2>
        <div className="cards">
          <div className="card">
            <img src="https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/4431452.png" alt="QB" />
            <div className="stat-number" data-target="2836">0</div>
            <h4>Passing Yards Leader:</h4>
            <p>Drake Maye</p>
          </div>
          <div className="card">
            <img src="https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/4429795.png" alt="RB" />
            <div className="stat-number" data-target="732">0</div>
            <h4>Rushing Yards Leader:</h4>
            <p>Jahmyr Gibbs</p>
          </div>
          <div className="card">
            <img src="https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/4361432.png" alt="WR" />
            <div className="stat-number" data-target="499">0</div>
            <h4>Receiving Yards Leader:</h4>
            <p>Romeo Doubs</p>
          </div>
          <div className="card">
            <img src="https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/3122132.png" alt="EDGE" />
            <div className="stat-number" data-target="15">0</div>
            <h4>Sacks Leader:</h4>
            <p>Myles Garrett</p>
          </div>
        </div>
      </section>

      <section className="section" id="trends">
        <h2>Trending Teams</h2>
        <div className="cards">
          <div className="card">Hottest Offense</div>
          <div className="card">Top Defense</div>
          <div className="card">Biggest Riser</div>
        </div>
      </section>

      <section className="section" id="predictions">
        <h2>Predictions Preview</h2>
        <div className="cards">
          <div className="card">Biggest Performance</div>
          <div className="card">Biggest Upset</div>
          <div className="card">Matchup of the Week</div>
        </div>
      </section>
    </>
  )
}

export default Home