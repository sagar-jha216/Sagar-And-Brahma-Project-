import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
// import arrowIcon from '../../../assets/arrow-icon.svg';
import myVideo from '../../../assets/Coverpage_bg_vd.mp4';
import maskWhite from '../../../assets/mask-white.svg';
import maskOrange from '../../../assets/mask-orange.svg';
import './Login.css';

function Login(props) {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState('');
	const history = useHistory();

	const handleLogin = (e) => {
		e.preventDefault();

		if (username === 'admin' && password === 'admin') {
			setError('');
			history.push('/Home'); // navigate to home page
		} else {
			setError('Invalid credentials. Please try again.');
		}
	};

	return (
		<div className="login-page">
			{/* Header remains transparent on the landing page */}

			<div className='mx-auto grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 pt-10 lg:mx-0 lg:max-w-none lg:grid-cols-2'>
				<div className='leftLoginSection flex'>

					<div className="">
						<div className="container text-white card-content">
							<div className="d-flex justify-content-center align-items-center">
								{/* New Column Wrapper */}
								<div className="flex flex-col align-items-center">
									<div className="rounded login-section card ">
										<h5>Please enter your Account Details</h5>

										<form onSubmit={handleLogin}>
											<div className="mb-3">
												<label htmlFor="username" className="form-label">
													Enter Username
												</label>
												<input
													type="text"
													className="form-control inputFieldCls"
													id="username"
													placeholder="username"
													value={username}
													onChange={(e) => setUsername(e.target.value)}
													required
												/>
											</div>

											<div className="mb-5">
												<label htmlFor="password" className="form-label">
													Enter Password
												</label>
												<input
													type="password"
													className="form-control inputFieldCls mb-4"
													id="password"
													placeholder="******"
													value={password}
													onChange={(e) => setPassword(e.target.value)}
													required
												/>
											</div>

											{error && <div className="error-cls text-danger">{error}</div>}
											<button type="submit" className="demo-btn">
												Sign In
											</button>
										</form>
									</div>

									{/* Arrow icons below login */}
									{/* <div className="arrowIconCls">
								{Array.from({ length: 6 }).map((_, index) => (
									<img key={index} src={arrowIcon} alt="arrow icon" className="mx-3" />
								))}
							</div> */}
								</div>
							</div>
						</div>
					</div>

				</div>
				<div className='rightVideoSection  flex'>


					<div class="overlay"></div>
					<video autoPlay loop muted className="loginVideoBg">
						<source src={myVideo} type="video/mp4" />
					</video>

					<div className=''>
						<img src={maskWhite} alt='Mask gray' className='maskWhiteImg' />
						<img src={maskOrange} alt='Mask orange' className='maskOrangeImg loginOrangMask' />
					</div>
				</div>
			</div>

		</div>
	);
}

export default Login;
