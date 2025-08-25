import React from 'react';
import DoughnutChartDashboard from "./DoughnutChartDashboard";
import BarChartDashboard from "./BarChartDashboard";



const ChartDataComp = () => {


  return (

    <div className="flex flex-col lg:flex-row gap-6 p-4 pl-0 pr-0">
      {/* Column 1 */}
      <div className="flex-1 bg-white shadow-md rounded-lg p-4">
        <h3 className="text-lg font-semibold mb-4 titleTextChart">Wastage by Merch-Category</h3>
        <BarChartDashboard category="Produce (Fresh)" />

      </div>

      {/* Column 2 */}
      <div className="flex-1 bg-white shadow-md rounded-lg p-4 relative doughnutChartBOx">
        <h3 className="text-lg font-semibold mb-4 titleTextChart">Waste % of COGS</h3>
        <DoughnutChartDashboard />
        <div className="absolute bottom-2 right-2 text-sm text-gray-600 bottomTitle">
          Total COGS ($) = $26.4M
        </div>
      </div>

      {/* Column 3 */}
      <div className="flex-1 bg-white shadow-md rounded-lg p-4">
        {/* Intentionally left blank */}
      </div>
    </div>

  );
};

export default ChartDataComp;
