import React from 'react';
import { Switch, Route, useLocation } from 'react-router-dom';
import Header from './Pages/CommonComponents/Header/header';
import Home from './Pages/Components/Home/Home';
import Footer from './Pages/CommonComponents/Footer/footer';
import LandingPage from './Pages/Components/LandingPage/LandingPage';
import Login from './Pages/Components/Login/Login';
import { DashboardProvider } from './Data/DashboardContext';
import DashboardLeaderBoard from './Pages/Components/Home/RetailLeaderBoard/DashboardPages/DashboardLeaderBoard';
import ImpactTracker from './Pages/Components/ImpactTracker/ImpactTracker';
import CommandCenter from './Pages/Components/CommandCenter/CommandCenter';
import ProtectedRoute from './Pages/Components/ProtectedRoute';

function App(props) {
	const location = useLocation();
	const hideHeaderFooter = location.pathname === '/' || location.pathname === '/Login' || location.pathname === '/Home';

	const headObj = {
		head: 'Header goes here',
		main: 'Collegue List',
		foot: 'Footer Goes Here',
	};

	const user = {
		name: 'Admin',
	};

	return (
		<div className="container pl-0 pr-0 position-relative transparentBg">
			{hideHeaderFooter && (
				<>
					{/* Background elements */}
				</>
			)}
			<div className={'mainDiv'}>
				{hideHeaderFooter ? (
					<div className="headerCls">
						<Header user={user} />
					</div>
				) : (
					<Header user={user} />
				)}
				<div className="mb-0 middleSec">
					<div className="cstMain">
						<DashboardProvider>
							<Switch>
								<Route exact path="/" component={() => <LandingPage />} />
								<Route exact path="/Login" component={() => <Login />} />
								<ProtectedRoute exact path="/Home" component={() => <Home />} />
								<ProtectedRoute exact path="/ImpactTracker" component={() => <ImpactTracker />} />
								<ProtectedRoute exact path="/CommandCenter" component={() => <CommandCenter />} />
								<ProtectedRoute exact path="/DashboardLeaderBoard" component={() => <DashboardLeaderBoard />} />
								<Route>
									<div>NOT FOUND</div>
								</Route>
							</Switch>
						</DashboardProvider>
					</div>
				</div>
				{!hideHeaderFooter && <Footer title={headObj.foot} />}
			</div>
		</div>
	);
}

export default App;