import { AlertTriangle } from 'lucide-react';
import { Link } from 'react-router-dom';
import homeIcon3 from '../../../../assets/homeImg03.svg';
import arrowImg from '../../../../assets/arrowIcon.svg';


const ImpactTracker = () => {

  return (
    <Link to="/ImpactTracker">
      <div className="shadow-lg homeCardBox rightCardHight">
        <img src={homeIcon3} alt='Home Icon 3' className='homeIconLeader' />
        {/* Title Section */}
        <div className="p-3">
          <div className="homeTitleSec">
            <h1 className="text-lg font-semibold text-gray-900 homeTitle">Impact Tracker <img src={arrowImg} alt='arrow' className='ml-2' /></h1>
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
                Quantifies the business value delivered—by tracking shrink prevented, margin gained and cost saved.
              </li>

            </ul>
          </div>
        </div>


      </div>
    </Link>
  );
};

export default ImpactTracker;