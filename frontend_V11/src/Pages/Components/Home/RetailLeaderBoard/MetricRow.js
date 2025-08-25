import { Link } from 'react-router-dom';
import { Package, Box, ShoppingCart } from 'lucide-react';
import ProgressBar from './ProgressBar';
import indicatorCatgoryPer from '../../../../assets/polygon-indicator.svg';

const categoryRouteMap = {
  Package: '/DashboardLeaderBoard',
  Box: '/DashboardLeaderBoard',
  ShoppingCart: '/DashboardLeaderBoard',
};

const iconMap = {
  Package: Package,
  Box: Box,
  ShoppingCart: ShoppingCart,
};

const MetricRow = ({ metric, isHoverable = true }) => {
  const IconComponent = iconMap[metric.icon] || Package;
  
   const ranges = metric.ranges
    ? [parseFloat(metric.ranges.low), parseFloat(metric.ranges.medium), parseFloat(metric.ranges.high)]
    : [0, 100];
  const minRange = Math.min(...ranges);
  const maxRange = Math.max(...ranges);
  const rawPercentage = parseFloat(metric.percentage);
  const clampedPercentage = Math.min(maxRange, Math.max(minRange, rawPercentage));
  let relativePercentage = ((clampedPercentage - minRange) / (maxRange - minRange)) * 100;
 
    const medium = parseFloat(metric.ranges?.medium?.replace('%', '') || 0);
    if (clampedPercentage === medium) {
    relativePercentage = 50;
    }
  

  const routeLink = categoryRouteMap[metric.icon] || '/Dashboard';

  return (
    <div className={`mb-2 ${isHoverable ? 'hover:transition-colors duration-200 p-2 rounded-lg -m-2 flex' : ''}`}>
      <div className="items-center justify-between mb-1 leftSecShrinkMetric">
        <div className="flex items-center gap-2">
          <IconComponent className="w-3 h-3 text-gray-400" />
          <Link to={routeLink} className="metricCatagoryText">
            {metric.category}
          </Link>
        </div>
        <div className="metricCatagoryPercentage">{metric.percentage}</div>
      </div>

      <div className="rightSecShrinkMetric relative w-full">
        <ProgressBar
          distribution={metric.distribution}
          showLabels={true}
          ranges={metric.ranges}
          percentage={metric.percentage}
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
            title={`${metric.percentage}`}
          />
        </div>
      </div>
    </div>
  );
};

export default MetricRow;
