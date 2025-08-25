import { AlertTriangle } from 'lucide-react';
import homeIcon2 from '../../../../assets/homeImg02.svg';
import arrowImg from '../../../../assets/arrowIcon.svg';
import arrowIcon from '../../../../assets/arrow-icon.svg';
import { Link } from 'react-router-dom';


const CommandCenter = (data) => {
  const { CommandCenterTopContent, shrinkageMetrics, inTransit, legend, dataSource } = data;
  return (
    <Link to="/CommandCenter">
      <div className="shadow-lg homeCardBox rightCardMarBt rightCardHight">
        <img src={homeIcon2} alt='Home Icon 2' className='homeIconLeader' />

        {/* Title Section */}
        <div className="p-3">
          <div className="homeTitleSec">
            <h1 className="text-lg font-semibold text-gray-900 homeTitle">Command Center <img src={arrowImg} alt='arrow' className='ml-2' /></h1>
            {/* <AlertTriangle className="w-4 h-4 text-warning-yellow" /> */}
          </div>
          {/* <p className="text-xs font-medium text-gray-600 uppercase tracking-wide mb-2">
          {HomeTopCardContent.subtitle}
        </p>
        <p className="text-xs text-gray-500">
          {HomeTopCardContent.description}
        </p> */}

          <div className='commandCenterContentSection'>
            <ul>
              <li>
                <img src={arrowIcon} className='arrowIcon' alt='arrowIcon' /> Provides shrink visibility across the retail value chain
              </li>
              <li><img src={arrowIcon} className='arrowIcon' alt='arrowIcon' /> Recommends cost effective remediation </li>
              <li><img src={arrowIcon} className='arrowIcon' alt='arrowIcon' /> Enables seamless cross functional communication</li>
            </ul>
          </div>
        </div>


      </div>
    </Link>
  );
};

export default CommandCenter;