import React from 'react';
import "./home.css";
import RetailLeaderBoard from "./RetailLeaderBoard/RetailLeaderBoard";
import CommandCenter from './CommandCenter/CommandCenter';
import { RetailLeaderBoardData } from '../../../Data/mockData';
import ImpactTracker from './ImpactTracker/ImpactTracker';
import homeVideo from '../../../assets/homeBGVideo.mp4';

// import CPIChart from '../Test/CPIChart';


function Home() {

    //const [isCollapsed, setIsCollapsed] = React.useState(false);

    // const toggleColumn = () => {
    //     setIsCollapsed(!isCollapsed);
    // };


    return <div className='cstHome container'>


        {/* <div className='row'>
            <div className='col-md-4 column'>test</div>
            <div className='col-md-4 column'>test</div>
            {isCollapsed && (
                <button className="expand-btn" onClick={toggleColumn}>
                    Expand Column 3
                </button>
            )}
            <div className='col-md-4 column'>



                <div className='innerContent'>


                    {!isCollapsed && (
                        <div className="column">
                            <button onClick={toggleColumn}>Collapse</button>
                            <p>This is Column 3</p>
                        </div>
                    )}


                </div>
            </div>
        </div> */}
        {/* <CPIChart /> */}
        <div className='homeBGVideoSection'>
            <div class="overlay"></div>
            <video autoPlay loop muted className="homeBG">
                <source src={homeVideo} type="video/mp4" />
            </video>
        </div>
        <div className='flex homeContentSec'>
            <div className='col-6 p-4'>
                <RetailLeaderBoard />
            </div>
            <div className='col-6 p-4'>

                <CommandCenter data={RetailLeaderBoardData} />
                <ImpactTracker />

            </div>

        </div>


    </div>
}

export default Home;
