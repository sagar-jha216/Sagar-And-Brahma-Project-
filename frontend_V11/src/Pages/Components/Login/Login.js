import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import myVideo from '../../../assets/Coverpage_bg_vd.mp4';
import maskWhite from '../../../assets/mask-white.svg';
import maskOrange from '../../../assets/mask-orange.svg';
import './Login.css';

const API_BASE_URL = process.env.REACT_APP_BASE_URL;

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
	const history = useHistory();
	

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await fetch(`${API_BASE_URL}/user/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include', 
                body: JSON.stringify({ userName:username, password }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Login failed');
            }

            const data = await response.json();
            if (data?.isAdmin) {
                console.log("sagar")
                history.push('/Home');
            } else {
                setError(data.message || 'Invalid credentials. Please try again.');
            }
        } catch (err) {
            console.error('Login error:', err);
            setError(err.message || 'Unable to connect to server. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page">
            <div className="mx-auto grid max-w-2xl grid-cols-1 gap-x-8 gap-y-16 pt-10 lg:mx-0 lg:max-w-none lg:grid-cols-2">
                <div className="leftLoginSection flex">
                    <div className="container text-white card-content">
                        <div className="d-flex justify-content-center align-items-center">
                            <div className="flex flex-col align-items-center">
                                <div className="rounded login-section card">
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
                                                disabled={loading}
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
                                                disabled={loading}
                                            />
                                        </div>

                                        {error && <div className="error-cls text-danger">{error}</div>}

                                        <button type="submit" className="demo-btn" disabled={loading}>
                                            {loading ? 'Signing In...' : 'Sign In'}
                                        </button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="rightVideoSection flex">
                    <div className="overlay"></div>
                    <video autoPlay loop muted className="loginVideoBg">
                        <source src={myVideo} type="video/mp4" />
                    </video>
                    <div>
                        <img src={maskWhite} alt="Mask gray" className="maskWhiteImg" />
                        <img src={maskOrange} alt="Mask orange" className="maskOrangeImg loginOrangMask" />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Login;




