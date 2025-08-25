import React, { useState } from 'react';
import './LandingPage.css';
// import logo from '../../../assets/logo.svg';
import arrowIcon from '../../../assets/arrow-icon.svg';
import myVideo from '../../../assets/Coverpage_bg_vd.mp4';
import maskGray from '../../../assets/mask-gray.svg';
import maskOrange from '../../../assets/mask-orange.svg';

const posts = [
	{
		id: 1,
		title: 'TRACKS',
		href: '#',
		description:
			'financial and operational impact of implemented action',
		date: 'Feb 12, 2020',
		datetime: '2020-02-12',
		category: { title: 'Business', href: '#' },
		author: {
			name: 'Tom Cook',
			role: 'Director of Product',
			href: '#',
			imageUrl:
				'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
		},
	},
	{
		id: 2,
		title: 'DETECTS ',
		href: '#',
		description:
			'shrink source',
		date: 'Mar 16, 2020',
		datetime: '2020-03-16',
		category: { title: 'Marketing', href: '#' },
		author: {
			name: 'Michael Foster',
			role: 'Co-Founder / CTO',
			href: '#',
			imageUrl:
				'https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
		},
	},
	
	{
		id: 3,
		title: 'NOTIFIES ',
		href: '#',
		description:
			'relevant team / stakeholder in one click',
		date: 'Feb 12, 2020',
		datetime: '2020-02-12',
		category: { title: 'Business', href: '#' },
		author: {
			name: 'Tom Cook',
			role: 'Director of Product',
			href: '#',
			imageUrl:
				'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
		},
	},

	{
		id: 4,
		title: 'RECOMMENDS ',
		href: '#',
		description: 'cost effective remediations',
		date: 'Mar 10, 2020',
		datetime: '2020-03-10',
		category: { title: 'Sales', href: '#' },
		author: {
			name: 'Lindsay Walton',
			role: 'Front-end Developer',
			href: '#',
			imageUrl:
				'https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
		},
	},
	
]


function LandingPage(props) {
	const [email, setEmail] = useState('');
	const [emailError, setEmailError] = useState('');

	// Basic email validation function
	const validateEmail = (email) => {
		const regex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
		return regex.test(email);
	};

	const handleSubmit = (e) => {
		e.preventDefault();
		if (!validateEmail(email)) {
			setEmailError('Please enter a valid email address.');
		} else {
			setEmailError('');
			// Process the email submission (e.g. send to backend)
		}
	};




	return (
		<div className="landing-page card-bg">
			<div className="card-section">
				<div className='lg:grid-cols-2 flex'>

					<div className='leftSection'>
						<div className="card-content">

							<div className="py-2 sm:py-7">
								<div className="mx-auto">
									<div className="mx-auto =lg:mx-0">
										<h2 className="text-4xl font-semibold tracking-tight text-pretty text-gray-900 sm:text-5xl titleTextLandingPage">Proactively <span className='redTextColor'>detect shrinkage</span> and implement <span className='orangeTextColor'>recommended remediation</span> to <span className='redTextColor'>prevent losses</span></h2>
										<p className="mt-2 text-lg/8 text-gray-600">Use data, AI, automation to predict shrink, prevent loss and improve profits</p>
									</div>
									<div className="mx-auto grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 pt-10 lg:mx-0 lg:max-w-none lg:grid-cols-4">
										{posts.map((post) => (
											<article key={post.id} className="flex max-w-xl flex-col items-start justify-between detailsBox">

												<div className="group relative grow">
													<h3 className="mt-3 text-lg/6 font-semibold text-gray-900 group-hover:text-gray-600 boxTitle">
														{/* <a href={post.href}>
													<span className="absolute inset-0" />
													{post.title}
												</a> */}

														{post.title}

													</h3>
													<p className="mt-1 mb-5 line-clamp-3 text-sm/6 descText">{post.description}</p>
													<img src={arrowIcon} className='arrowIcon' alt='arrowIcon' />
												</div>

											</article>
										))}
									</div>
								</div>
							</div>
							{/* Email Form */}
							<form className="email-form" onSubmit={handleSubmit}>
								<div className="flex g-2 mt-10">
									<div className="">
										<input
											type="email"
											className="form-control email-input rounded-pill fs-14"
											placeholder="Enter your email address"
											value={email}
											onChange={(e) => setEmail(e.target.value)}
											required
										/>
										{emailError && <div className="invalid-feedback">{emailError}</div>}
									</div>
									<div className="">
										<button type="submit" className="demo-btn rounded-pill fs-14">
											Book Demo
										</button>
									</div>
									<div className="mt-3 d-flex arrowCls">
										{/* {Array.from({ length: 6 }).map((_, index) => (
									<img key={index} src={arrowIcon} alt="arrow icon" className="mr-3" />
								))} */}
									</div>
								</div>
							</form>

							{/* Partnership Section
					<div className="partnership">
						<p>Collaboration with data provider</p>
						<img src={partnerLogo} alt="Partner Logo" className="partner-logo" />
					</div> */}
						</div>
					</div>

					<div className='rightSection'>
						<div class="overlay"></div>
						<video autoPlay loop muted className="videoBg">
							<source src={myVideo} type="video/mp4" />
						</video>

						<div className=''>
							<img src={maskGray} alt='Mask gray' className='maskGrayImg'/>
							<img src={maskOrange} alt='Mask orange' className='maskOrangeImg'/>
						</div>
					</div>


				</div>

			</div>
		</div>
	);
}
export default LandingPage;
