import {useEffect,useState} from "react"
import { AlertTriangle } from 'lucide-react';
import MetricRow from './MetricRow';
import ProgressBar from './ProgressBar';
import homeIcon1 from '../../../../assets/homeImg01.svg';
import arrowImg from '../../../../assets/arrowIcon.svg';
import indicatorCatgoryPer from '../../../../assets/polygon-indicator.svg';
import ShrinkageService from "../../../../services/shrinkageService";

const LeaderDashboardCard = ({ data }) => {
  // const { LeaderBoardTopContent, shrinkageMetrics, inTransit, legend, dataSource } = data
  const [leaderBoardData, setLeaderBoardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const apiData = await ShrinkageService.fetchRetailLeaderBoardData();
        const transformedData = ShrinkageService.transformToFrontendFormat(apiData);
        setLeaderBoardData(transformedData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!leaderBoardData) return null; // or a fallback UI
  
  const {LeaderBoardTopContent,shrinkageMetrics,inTransit,legend,dataSource}=leaderBoardData;

  const ranges = inTransit.ranges
    ? [parseFloat(inTransit.ranges.low), parseFloat(inTransit.ranges.medium), parseFloat(inTransit.ranges.high)]
    : [0, 100];
  const minRange = Math.min(...ranges);
  const maxRange = Math.max(...ranges);
  const rawPercentage = parseFloat(inTransit.percentage);
  const clampedPercentage = Math.min(maxRange, Math.max(minRange, rawPercentage));
  let relativePercentage = ((clampedPercentage - minRange) / (maxRange - minRange)) * 100;

  const medium = parseFloat(inTransit.ranges?.medium?.replace('%', '') || 0);
  if (clampedPercentage === medium) {
    relativePercentage = 50;
  }

  return (
    <div className="shadow-lg homeCardBox">
      <img src={homeIcon1} alt='Home Icon' className='homeIconLeader' />
      {/* Header Section */}
      {/* <div className="bg-brand-red px-4 py-3 flex items-center justify-center">
        <div className="bg-white rounded px-2 py-1">
          <span className="text-brand-red font-bold text-sm">III</span>
        </div>
      </div> */}

      {/* Title Section */}
      <div className="p-3">
        <div className="flex items-center gap-2 mb-1 homeTitleSec">
          <h1 className="text-lg font-semibold text-gray-900 retalLeadertext">{LeaderBoardTopContent.title} <img src={arrowImg} alt='arrow' className='ml-2' /> </h1>
          {/* <AlertTriangle className="w-4 h-4 text-warning-yellow" /> */}
        </div>
        <p className="text-xs font-medium text-gray-600 uppercase tracking-wide mb-2 homeSubTitle">
          {LeaderBoardTopContent.subtitle}
        </p>
        <p className="text-xs text-gray-500 homeDecText">
          {LeaderBoardTopContent.description}
        </p>
      </div>

      {/* Shrinkage Section */}
      <div className="p-4">
        <div className="mb-4">
          <h2 className="homeTitleParentSec"><span className='homeSubTitleSec'>Shrinkage %</span></h2>

          {shrinkageMetrics.map(metric => (
            <MetricRow key={metric.id} metric={metric} />
          ))}
        </div>

        {/* In-Transit Section */}
        <div className="rounded-lg mb-3 ">
          <div className=" items-center justify-between mb-1 homeTitleParentSec">
            <span className='homeSubTitleSec'>
              <span className="text-white text-sm font-medium mr-2">{inTransit.title}</span>
              <span className="text-white text-sm font-bold colorOrg">{inTransit.percentage}</span>
            </span>
          </div>
          {/* <div className="w-full bg-gray-600 rounded-full h-2 mb-2">
            <div className="flex h-2 rounded-full overflow-hidden">
              <div 
                className="bg-success-green" 
                style={{ width: `${inTransit.distribution.green}%` }}
              ></div>
               
              <div 
                className="bg-warning-yellow" 
                style={{ width: `${inTransit.distribution.yellow}%` }}
              ></div>
              <div 
                className="bg-brand-red" 
                style={{ width: `${inTransit.distribution.red}%` }}
              ></div>
            </div>
          </div> */}

          <div className='flex mb-4'>
            <div className='leftSecBox'></div>
            <div className='rightSecBox'>
              <ProgressBar
                distribution={inTransit.distribution}
                ranges={inTransit.ranges}
                showLabels={true}
              />
              <div className="relative w-full">
                <img
                  src={indicatorCatgoryPer}
                  alt="Indicator"

                  className="absolute indicatorImg w-4 h-4"
                  style={{
                    left: `${relativePercentage}%`,
                    transform: 'translateX(-50%)',
                  }}
                  title={`${inTransit.percentage}`}
                />
              </div>
            </div>

          </div>

          <div className='flex '>
            <div className='leftSecBox'>
              {/* Source Section */}
              <div className="text-center">
                <span className="text-gray-400 dataSourceText">{dataSource}</span>
              </div>

            </div>
            <div className='rightSecBox'>
              {/* Legend Section */}
              <div className="flex items-center justify-center gap-4 mb-2 mt-2 text-xs">

                {legend.map((item, index) => (
                  <div key={index} className="flex items-center gap-1">
                    <div className={`w-3 h-3 rounded-full ${item.color === 'green' ? 'bg-success-green' :
                      item.color === 'yellow' ? 'bg-warning-yellow' :
                        'bg-brand-red'
                      }`}></div>
                    <span className="text-gray-600">{item.label}</span>
                  </div>
                ))}
              </div>
            </div>

          </div>



          {/* <div className="flex justify-between text-xs text-gray-400">
            <span>{inTransit.ranges.low}</span>
            <span>{inTransit.ranges.medium}</span>
            <span>{inTransit.ranges.high}</span>
          </div> */}
        </div>

        {/* Legend Section */}
        {/* <div className="flex items-center justify-center gap-4 mb-3 text-xs">

          {legend.map((item, index) => (
            <div key={index} className="flex items-center gap-1">
              <div className={`w-3 h-3 rounded-full ${item.color === 'green' ? 'bg-success-green' :
                item.color === 'yellow' ? 'bg-warning-yellow' :
                  'bg-brand-red'
                }`}></div>
              <span className="text-gray-600">{item.label}</span>
            </div>
          ))}
        </div> */}

        {/* Source Section */}
        {/* <div className="text-center">
          <span className="text-xs text-gray-400">{dataSource}</span>
        </div> */}
      </div>
    </div>
  );
};

export default LeaderDashboardCard;
