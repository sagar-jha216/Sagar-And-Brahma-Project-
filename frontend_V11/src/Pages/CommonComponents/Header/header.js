// import React, { useEffect } from 'react';
// import { Link, useLocation, useHistory } from 'react-router-dom';
// import './header.css';
// import logo from '../../../assets/genpactLogo.svg';
// import ShrinkLogo from "../../../assets/ShrinkLogo.png";
// import userIcon from '../../../assets/defaultUser.svg';

// function Header({ user }) {
// 	const location = useLocation();
// 	const history = useHistory();
// 	const [showMenu, setShowMenu] = React.useState(false);
// 	const [dropdownOpen, setDropdownOpen] = React.useState(false);
// 	const isLandingOrLogin = location.pathname === '/' || location.pathname === '/Login';

// 	const toggleDropdown = () => {
// 		setDropdownOpen(!dropdownOpen);
// 	};

// 	const routeHome = () => {
// 		if (location.pathname !== '/' || location.pathname !== '/Login' || location.pathname !== '/Home') {
// 			history.push('/Home');
// 		}
// 	};

// 	const closeDropdown = () => {
// 		setDropdownOpen(false);
// 		history.push('/Login');
// 	};

// 	useEffect(() => {
// 		if (location.pathname !== '/' || location.pathname !== '/Login' || location.pathname !== '/Home') {
// 			setShowMenu(true);
// 		} else {
// 			setShowMenu(false);
// 		}
// 	}, [location.pathname]);

// 	const DashboardSelection = (path) => {
// 		switch (path) {
// 			case '/Dashboard':
// 				return 'selected';
// 			case '/sku':
// 				return 'selected';
// 			case '/sku/list':
// 				return 'selected';
// 			case '/sku_bundle':
// 				return 'selected';
// 			default:
// 				return '';
// 		}
// 	};

// 	return (
// 		<div className={`cstHeader ${isLandingOrLogin ? 'site-header' : 'bg-dark'}`}>
// 			<div className="logo-section">
// 				<img
// 					src={logo}
// 					alt="Genpact Logo"
// 					className="logo"
// 					onClick={() => {
// 						routeHome();
// 					}}
// 				/><span className='sapLine'></span>
// //                 <span className='titleText'><img src={ShrinkLogo} alt='siteLogo' /></span>
// 			</div>
// 			{location.pathname === '/' || location.pathname === '/Login' || location.pathname === '/Home' ? (
// 				<nav className="nav-links">
// 					{/* <Link to={window.location.pathname} className="hiw-css">
// 						How it works?
// 					</Link> */}
// 					{location.pathname === '/' && (
// 						<Link to="/Login" className="demo-btn rounded-pill fs-14 text-Primiary">
// 							Log In
// 						</Link>
// 					)}
// 				</nav>
// 			) : showMenu ? (
// 				<div className="menuSec">
// 					{/* <Link className={DashboardSelection(location.pathname)} to="/Dashboard">
// 						Dashboard
// 					</Link>
// 					<Link
// 						className={location.pathname === '/PricingSimulator' ? 'selected' : ''}
// 						to="/PricingSimulator"
// 					>
// 						Pricing Simulator
// 					</Link>
// 					<Link className={location.pathname === '/GeoStrategy' ? 'selected' : ''} to="/GeoStrategy">
// 						Geo Strategy
// 					</Link>
// 					<Link
// 						className={location.pathname === '/PricingPerformance' ? 'selected' : ''}
// 						to="/PricingPerformance"
// 					>
// 						Pricing Performance
// 					</Link>
// 					<Link
// 						className={location.pathname === '/HolidaysandPromotions' ? 'selected' : ''}
// 						to="/HolidaysandPromotions"
// 					>
// 						Holidays and Promotions
// 					</Link> */}
// 				</div>
// 			) : null}

// 			{!isLandingOrLogin && (
// 				<div
// 					className="userDetails"
// 					onMouseEnter={() => setDropdownOpen(true)}
// 					onMouseLeave={() => setDropdownOpen(false)}
// 				>
// 					<span className="userName">Good Afternoon, {user.name}</span>
// 					<img src={userIcon} alt="User Icon" className="userIcon" />
// 					<svg
// 						xmlns="http://www.w3.org/2000/svg"
// 						width="16"
// 						height="16"
// 						fill="white"
// 						className={`arrowIcon ${dropdownOpen ? 'rotate' : ''}`}
// 						viewBox="0 0 16 16"
// 					>
// 						<path
// 							fillRule="evenodd"
// 							d="M8 4a.5.5 0 0 1 .5.5v5.793l2.146-2.147a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-3-3a.5.5 0 1 1 .708-.708L7.5 10.293V4.5A.5.5 0 0 1 8 4"
// 						/>
// 					</svg>
// 					{dropdownOpen && (
// 						<div className="dropdownMenu">
// 							<ul>
// 								<li className="">
// 									<div className="userNameText">{user.name}</div>
// 									<div className="userDesignation">(Category Manager)</div>
// 								</li>
// 								<li>
// 									<div className="logoutText" onClick={closeDropdown}>
// 										Logout
// 									</div>
// 								</li>
// 							</ul>
// 						</div>
// 					)}
// 				</div>
// 			)}
// 		</div>
// 	);
// }

// export default Header;

import React, { useEffect, useState } from 'react';
import { Link, useLocation, useHistory, NavLink } from 'react-router-dom';
import './header.css';
import logo from '../../../assets/GLogo.svg';
import logoG from '../../../assets/genpactLogo.svg';
import ShrinkLogo from "../../../assets/ShrinkLogo.png";
import userIcon from '../../../assets/defaultUser.svg';


function Header({ user }) {
	const location = useLocation();
	const history = useHistory();
	const [showMenu, setShowMenu] = React.useState(false);
	const [dropdownOpen, setDropdownOpen] = React.useState(false);

	const [refreshTime, setRefreshTime] = useState('');

	// useEffect(() => {
	// 	const now = new Date();
	// 	const options = {
	// 		year: 'numeric',
	// 		month: '2-digit',
	// 		day: '2-digit',
	// 		hour: '2-digit',
	// 		minute: '2-digit',
	// 		second: '2-digit',
	// 		hour12: true,
	// 		//timeZone: 'America/Chicago',
	// 		timeZoneName: 'short'
	// 	};

	// 	const formatted = now.toLocaleString('en-US', options);
	// 	setRefreshTime(formatted);
	// }, []);

	
useEffect(() => {
    const now = new Date();
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
        // timeZone: 'Asia/Kolkata',
        timeZoneName: 'short'
    };

    const formatted = now.toLocaleString('en-US', options);
    setRefreshTime(formatted);
}, []);

	const isLandingOrLogin = location.pathname === '/' || location.pathname === '/Login';

	const hideSapLine = location.pathname === '/' || location.pathname === '/Login' || location.pathname === '/Home';

	const hideSapLineIntial = location.pathname === '/Home' || location.pathname === '/ImpactTracker' || location.pathname === '/CommandCenter' || location.pathname === '/DashboardLeaderBoard';

	const getActivePageName = (path) => {
		switch (path) {
			case '/CommandCenter':
				return 'Command Center';
			case '/ImpactTracker':
				return 'Impact Tracker';
			case '/DashboardLeaderBoard':
				return 'Leader Board';
			default:
				return '';
		}
	};


	const toggleDropdown = () => {
		setDropdownOpen(!dropdownOpen);
	};

	const routeHome = () => {
		if (location.pathname !== '/' || location.pathname !== '/Login' || location.pathname !== '/Home') {
			history.push('/Home');
		}
	};

	const closeDropdown = () => {
		setDropdownOpen(false);
		history.push('/Login');
	};

	useEffect(() => {
		if (location.pathname !== '/' || location.pathname !== '/Login' || location.pathname !== '/Home') {
			setShowMenu(true);
		} else {
			setShowMenu(false);
		}
	}, [location.pathname]);

	// const DashboardSelection = (path) => {
	// 	switch (path) {
	// 		case '/Dashboard':
	// 			return 'selected';
	// 		case '/sku':
	// 			return 'selected';
	// 		case '/sku/list':
	// 			return 'selected';
	// 		case '/sku_bundle':
	// 			return 'selected';
	// 		default:
	// 			return '';
	// 	}
	// };

	return (
		
		<div className={`cstHeader ${isLandingOrLogin
				? 'site-header'
				: (['/CommandCenter', '/ImpactTracker', '/DashboardLeaderBoard'].includes(location.pathname) ? 'bg-white' : 'bg-dark')
			}`}>

			<div className="logo-section">
				
				<img
					src={isLandingOrLogin ? logoG : logo}  
					alt="G Logo"
					className={isLandingOrLogin ? "logo-large" : "logo"}  
					onClick={() => {
						routeHome();
					}}
				/>
				
{!hideSapLineIntial && <span className='sapLine'></span>}
				<span className='titleText'>
					<img
						src={ShrinkLogo}
						alt='siteLogo'
						className={isLandingOrLogin ? "shrinkLogo-large" : ""}
					/>
				</span>



				{!hideSapLine && <span className='sapLine'></span>}


				{!isLandingOrLogin && (
					<div className="nav-links active-page-name">
						{getActivePageName(location.pathname)}
					</div>
				)}

			</div>


			{!isLandingOrLogin && (
				<div className="nav-links">
					<div className="last-refresh">
						<strong>Last Refresh: </strong> {refreshTime}
					</div>
				</div>
			)}



			{location.pathname === '/' || location.pathname === '/Login' || location.pathname === '/Home' ? (
				<nav className="nav-links">
					
					{location.pathname === '/' && (
						<Link to="/Login" className="demo-btn rounded-pill fs-14 text-Primiary">
							Log In
						</Link>
					)}
				</nav>
			) : showMenu ? (
				<div className="menuSec">

				</div>
			) : null}



			{!isLandingOrLogin && (
				<div
					className="userDetails"
					onMouseEnter={() => setDropdownOpen(true)}
					onMouseLeave={() => setDropdownOpen(false)}
				>

					<span className="userName">
						Welcome,<br />
						<span className="userNameRight"> <strong>{user.name}</strong></span>
					</span>
					<img src={userIcon} alt="User Icon" className="userIcon" />

					{dropdownOpen && (
						<div className="dropdownMenu">
							<ul>
								<li className="">
									<div className="userNameText">{user.name}</div>
									<div className="userDesignation">(Category Manager)</div>
								</li>
								<li>
									<div className="logoutText" onClick={closeDropdown}>
										Logout
									</div>
								</li>
							</ul>
						</div>
					)}
				</div>
			)}
		</div>
	);
}

export default Header;

