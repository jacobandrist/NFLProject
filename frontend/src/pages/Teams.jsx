import { Link } from 'react-router-dom'

function Teams() {
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

      <main>
        <section className="All-Teams">
          <h2>NFL Teams</h2>
          <div className="divisions">
            <div className="division">
              <h3>NFC North</h3>
              <hr/>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Chicago_Bears_logo.svg/2560px-Chicago_Bears_logo.svg.png" alt="Bears"/>
                <h4>Chicago Bears</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/7/71/Detroit_Lions_logo.svg" alt="Lions"/>
                <h4>Detroit Lions</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Green_Bay_Packers_logo.svg/2560px-Green_Bay_Packers_logo.svg.png" alt="Packers"/>
                <h4>Green Bay Packers</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/4/48/Minnesota_Vikings_logo.svg/977px-Minnesota_Vikings_logo.svg.png" alt="Vikings"/>
                <h4>Minnesota Vikings</h4>
              </div>
            </div>

            <div className="division">
              <h3>NFC East</h3>
              <hr/>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Dallas_Cowboys.svg" alt="Cowboys"/>
                <h4>Dallas Cowboys</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/8/8e/Philadelphia_Eagles_logo.svg" alt="Eagles"/>
                <h4>Philadelphia Eagles</h4>
              </div>
              <div className="team">
                <img src="https://logos-world.net/wp-content/uploads/2020/05/New-York-Giants-Logo.png" alt="Giants"/>
                <h4>New York Giants</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Washington_Commanders_logo.svg/2560px-Washington_Commanders_logo.svg.png" alt="Commanders"/>
                <h4>Washington Commanders</h4>
              </div>
            </div>

            <div className="division">
              <h3>NFC South</h3>
              <hr/>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/c/c5/Atlanta_Falcons_logo.svg/1200px-Atlanta_Falcons_logo.svg.png" alt="Falcons"/>
                <h4>Atlanta Falcons</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/1/1c/Carolina_Panthers_logo.svg/1200px-Carolina_Panthers_logo.svg.png" alt="Panthers"/>
                <h4>Carolina Panthers</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/New_Orleans_Saints_logo.svg/985px-New_Orleans_Saints_logo.svg.png" alt="Saints"/>
                <h4>New Orleans Saints</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/a/a2/Tampa_Bay_Buccaneers_logo.svg" alt="Buccaneers"/>
                <h4>Tampa Bay Buccaneers</h4>
              </div>
            </div>

            <div className="division">
              <h3>NFC West</h3>
              <hr/>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/7/72/Arizona_Cardinals_logo.svg/1200px-Arizona_Cardinals_logo.svg.png" alt="Cardinals"/>
                <h4>Arizona Cardinals</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/8/8a/Los_Angeles_Rams_logo.svg" alt="Rams"/>
                <h4>Los Angeles Rams</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/commons/3/3a/San_Francisco_49ers_logo.svg" alt="49ers"/>
                <h4>San Francisco 49ers</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/8/8e/Seattle_Seahawks_logo.svg/1200px-Seattle_Seahawks_logo.svg.png" alt="Seahawks"/>
                <h4>Seattle Seahawks</h4>
              </div>
            </div>

            <div className="division">
              <h3>AFC North</h3>
              <hr/>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/1/16/Baltimore_Ravens_logo.svg/1200px-Baltimore_Ravens_logo.svg.png" alt="Ravens"/>
                <h4>Baltimore Ravens</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/81/Cincinnati_Bengals_logo.svg" alt="Bengals"/>
                <h4>Cincinnati Bengals</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/d/d9/Cleveland_Browns_logo.svg" alt="Browns"/>
                <h4>Cleveland Browns</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Pittsburgh_Steelers_logo.svg/1200px-Pittsburgh_Steelers_logo.svg.png" alt="Steelers"/>
                <h4>Pittsburgh Steelers</h4>
              </div>
            </div>

            <div className="division">
              <h3>AFC East</h3>
              <hr/>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/7/77/Buffalo_Bills_logo.svg" alt="Bills"/>
                <h4>Buffalo Bills</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/3/37/Miami_Dolphins_logo.svg" alt="Dolphins"/>
                <h4>Miami Dolphins</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/New_England_Patriots_logo.svg/1200px-New_England_Patriots_logo.svg.png" alt="Patriots"/>
                <h4>New England Patriots</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/New_York_Jets_2024.svg/1200px-New_York_Jets_2024.svg.png" alt="Jets"/>
                <h4>New York Jets</h4>
              </div>
            </div>

            <div className="division">
              <h3>AFC South</h3>
              <hr/>
              <div className="team">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTmttymFG_vta0RLbpQPYR4vmpHCkOiATeMOA&s" alt="Texans"/>
                <h4>Houston Texans</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Indianapolis_Colts_logo.svg/1141px-Indianapolis_Colts_logo.svg.png" alt="Colts"/>
                <h4>Indianapolis Colts</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/7/74/Jacksonville_Jaguars_logo.svg/1200px-Jacksonville_Jaguars_logo.svg.png" alt="Jaguars"/>
                <h4>Jacksonville Jaguars</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/c/c1/Tennessee_Titans_logo.svg/1200px-Tennessee_Titans_logo.svg.png" alt="Titans"/>
                <h4>Tennessee Titans</h4>
              </div>
            </div>

            <div className="division">
              <h3>AFC West</h3>
              <hr/>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/4/44/Denver_Broncos_logo.svg" alt="Broncos"/>
                <h4>Denver Broncos</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/e/e1/Kansas_City_Chiefs_logo.svg/1200px-Kansas_City_Chiefs_logo.svg.png" alt="Chiefs"/>
                <h4>Kansas City Chiefs</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/4/48/Las_Vegas_Raiders_logo.svg/1130px-Las_Vegas_Raiders_logo.svg.png" alt="Raiders"/>
                <h4>Las Vegas Raiders</h4>
              </div>
              <div className="team">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Los_Angeles_Chargers_logo.svg/1200px-Los_Angeles_Chargers_logo.svg.png" alt="Chargers"/>
                <h4>Los Angeles Chargers</h4>
              </div>
            </div>
          </div>
        </section>
      </main>
    </>
  )
}

export default Teams