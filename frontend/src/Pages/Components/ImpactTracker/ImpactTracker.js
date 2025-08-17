import React, { useState } from "react";
import { impactData } from "./ImpactTrackerData"; 
import "./ImpactTracker.css";
import { Filters } from "./Filters";
import alertIcon from "../../../assets/ImpactTracker/Alert_icon.svg"
import clockIcon from "../../../assets/ImpactTracker/Time-Icon.svg"
import calenderIcon from "../../../assets/ImpactTracker/Frequency_icon.svg";
import { southData } from "./ImpactTrackerData";
import { eastData } from "./ImpactTrackerData";
import { westData } from "./ImpactTrackerData";

const ImpactTracker = () => {
  const [filters, setFilters] = useState({
  region: "North",          
  selectedStores: [],
  selectedChannels: [],
  dateRange: [null, null],
});

const getFilteredData = ({ region, selectedChannels }) => {
  if (region === "South") {
    return southData;
  }
  else if (region === "East") {
    return eastData;
  }
  else if (region === "West") {
    return westData;
  }

  return impactData; 
};


const handleApplyFilters = (selectedFilters) => {
  setFilters(selectedFilters);
  const filteredData = getFilteredData(selectedFilters);
  setData(filteredData);
};

  const [data, setData] = useState(impactData);

  return (
    <main className="w-full background">
      {/* Filters - Full width, no padding */}
      <Filters onApply={handleApplyFilters} />

      {/* Content area with padding */}
      <div className="pt-0 pr-6 pb-6 pl-6">
        {/* Summary Cards */}
        <section className="cards flex flex-wrap gap-4 mb-6">
          <SummaryCard
            title="Todays Loss Mitigation"
            amount={data.summary.todaysLossMitigation}
            prefix="$"
            suffix="K"
            percentage={data.summary.todaysLossMitigationComparison.percentage}
            trendDirection={data.summary.todaysLossMitigationComparison.trendDirection}
            compareTo={data.summary.todaysLossMitigationComparison.compareTo}
            showChart={true} 
          />

          <SummaryCard
            title="Month To Date Loss Mitigation"
            amount={data.summary.monthToDateLossMitigation}
            prefix="$"
            suffix="K"
            percentage={data.summary.monthToDateLossMitigationComparison.percentage}
            trendDirection={data.summary.monthToDateLossMitigationComparison.trendDirection}
            compareTo={data.summary.monthToDateLossMitigationComparison.compareTo}
            showChart={true} 
          />

          <SummaryCard
            title="Year To Date Loss Mitigation"
            amount={data.summary.yearToDateLossMitigation}
            prefix="$"
            suffix="K"
            percentage={data.summary.yearToDateLossMitigationComparison.percentage}
            trendDirection={data.summary.yearToDateLossMitigationComparison.trendDirection}
            compareTo={data.summary.yearToDateLossMitigationComparison.compareTo}
            showChart={true} 
          />

          <SummaryCard
            title="Shrinkage Alerts Triggered"
            amount={data.summary.shrinkageAlertsTriggered}
            icon={alertIcon} 
          />

          <SummaryCard
            title="Avg. Time For Resolution"
            amount={data.summary.avgTimeForResolution}
            suffix=" Days"
            icon={calenderIcon} 
          />

          <SummaryCard
            title="Incident Frequency"
            amount={data.summary.incidentFrequency}
            icon={clockIcon} 
          />
        </section>

        {/* Charts */}
        <section className="flex gap-6 mb-6">
          <BarChart
            title="Last 7 Days Loss Mitigation"
            data={data.last7DaysLossMitigation}
          />
          <BarChart
            title="Monthly Loss Mitigation Per Store (Top 10)"
            data={data.monthlyLossMitigationPerStore}
          />
        </section>

        {/* Table */}
        <ShrinkReportTable data={data.weeklyShrinkReport} />
      </div>
    </main>
  );
};




const SummaryCard = ({
  title,
  amount,
  prefix = "",
  suffix = "",
  percentage,
  trendDirection,
  compareTo,
  showChart = false,
  icon,
}) => {
  let displayValue = amount;
  let displaySuffix = suffix;

  
  if (amount >= 1_000_000) {
    displayValue = (amount / 1_000_000).toFixed(1);
    displaySuffix = "M";
  } else if (amount >= 1_000) {
    displayValue = (amount / 1_000).toFixed(1);
    displaySuffix = "K";
  }

  let displayValueStr = displayValue.toString();

  if (displayValueStr.endsWith(".0")) {
    displayValueStr = displayValueStr.slice(0, -2);
  }

  

  const hasTrend = percentage !== undefined && trendDirection && compareTo;
  const isUp = trendDirection === "up";

  return (
    <div
      className="card-box bg-white p-4 rounded shadow border min-w-[170px] max-w-[180px] basis-[260px]"
      style={{
        display: "grid",
        gridTemplateRows: "28px 40px 24px 1fr", 
      }}
    >
      {/* Title */}
      <div className="overflow-hidden leading-tight text-sm font-semibold text-gray-800 title-move-up">
        {title}
      </div>

      {/* Amount + Bar chart/Icon side by side */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <p className="text-2xl font-bold text-black m-0">
          {prefix}
          {displayValueStr}
          {displaySuffix === " Days" ? (
            <span className="suffix-style">{displaySuffix}</span>
          ) : (
            displaySuffix
          )}
        </p>

        {showChart ? (
          <div className="flex items-end gap-0.5 w-14 h-13 mt-8 pl-3">
            {[2, 5, 6, 4, 7, 3].map((v, i) => (
              <div
                key={i}
                className="bg-[#FFAD28]  w-1.5"
                style={{ height: `${v * 6}px` }}
              />
            ))}
          </div>
        ) : icon ? (
          <img src={icon} alt="" className="w-9 h-9 mt-11 ml-2" />
            
        ) : null}
      </div>

      {/* Comparison (percentage + vs) below amount */}
      <div className="flex items-center">
        {hasTrend ? (
          <div className="flex items-center text-sm text-gray-600">
            <span
              className={`font-semibold flex items-center ${
                isUp ? "text-green-600" : "text-red-600"
              }`}
            >
              {Math.abs(percentage)}%
              <span className="ml-1">{isUp ? "▲" : "▼"}</span>
            </span>
            <span className="ml-2">vs {compareTo}</span>
          </div>
        ) : null}
      </div>

      
    </div>
  );
};


const BarChart = ({ title, data }) => {
  const chartHeight = 130;

  const cleanData = data.map((d) => ({
    ...d,
    value: Number(d.value),
  }));

  const maxValue = Math.max(...cleanData.map((d) => d.value)) || 1;
  const yMax = Math.ceil(maxValue / 1000) * 1000;

  const getYLabels = (max) => {
  const roundedMax = Math.ceil(max / 1000) * 1000;

  if (roundedMax <= 5000) {
    
    const step = 1000;
    const labels = [];
    for (let i = 0; i <= roundedMax; i += step) {
      labels.push(i);
    }
    return labels.reverse();
  } else {
    
    return [0, roundedMax / 2, roundedMax].reverse();
  }
};

  const yLabels = getYLabels(maxValue);

  return (
    <div className="bg-white p-4  graph-box flex-1 min-h-[240px]">
      <h3 className="font-semibold graph-title mb-7 text-black">{title}</h3>

      <div className="relative flex h-40 pl-2 pr-2">
        {/* Y-axis labels */}
        <div className="flex flex-col justify-between items-end mr-2 text-[10px] mt-1 font-normal text-gray-600 h-[130px]">
          {yLabels.map((val, i) => (
            <div key={i} className="leading-none">
              ${val / 1000}k
            </div>
          ))}
        </div>

        {/* Y-axis and X-axis lines */}
        <div className="absolute left-[34px] bottom-4 top-0 border-l border-gray-400 z-0" />
        <div className="absolute left-[34px] bottom-4 right-0 border-t border-gray-400 z-0" />

        {/* Bars */}
        <div className="flex justify-between items-end h-full pl-4 pr-2 w-full">
          {cleanData.map((d, i) => {
            const barHeight = Math.round((d.value / yMax) * chartHeight);

            return (
              <div key={i} className="flex flex-col items-center w-[40px] z-10">
                {/* Value label above bar */}
                <span className="text-xs font-semibold mb-0 text-gray-700">
                  {d.value >= 1000 ? `${(d.value / 1000).toFixed(1)}k` : d.value}
                </span>

                {/* Bar */}
                <div
                  className="bg-[#333] w-full"
                  style={{ height: `${barHeight}px` }}
                  title={`$${d.value.toLocaleString()}`}
                ></div>

                {/* Label below bar */}
                <span className="text-[9px] font-normal mt-1 text-gray-600">
                  {d.date || d.store}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
const ShrinkReportTable = ({ data }) => (
  <section className="mb-6">
    {/* Title and table wrapper */}
    <div className="bg-white  p-4 overflow-x-auto table-container">
      {/* Title aligned to table */}
      <h2 className="text-lg font-semibold text-black mb-4 table-title">
        Weekly Shrink Report
      </h2>

      <table className="min-w-full text-sm text-left border-separate border-spacing-0">
        <thead className="bg-[#ffad28] text-black">
          <tr>
            <th className="px-4 py-3 whitespace-nowrap">Date</th>
            <th className="px-4 py-3 whitespace-nowrap">Store/Location</th>
            <th className="px-4 py-3 whitespace-nowrap">Shrinkage Type</th>
            <th className="px-4 py-3 whitespace-nowrap">Estimated Loss ($)</th>
            <th className="px-4 py-3 whitespace-nowrap">Root Cause</th>
            <th className="px-4 py-3 whitespace-nowrap">Action Taken</th>
            <th className="px-4 py-3 whitespace-nowrap">Impact Score (1–5)</th>
            <th className="px-4 py-3 whitespace-nowrap">Follow-up Date</th>
          </tr>
        </thead>

        <tbody>
          {data.map((row, idx) => (
            <tr
              key={idx}
              className={`${
                idx % 2 === 0 ? "bg-[#fff2df]" : "bg-white"
              } border-b border-black table-text`}
            >
              <td className="table-cell whitespace-nowrap">{row.date}</td>
              <td className="table-cell whitespace-nowrap">{row.store}</td>
              <td className="table-cell">{row.shrinkageType}</td>
              <td className="table-cell">
                ${row.estimatedLoss.toLocaleString()}
              </td>
              <td className="table-cell">{row.rootCause}</td>
              <td className="table-cell">{row.actionTaken}</td>
              <td className="table-cell">{row.impactScore}</td>
              <td className="table-cell">{row.followUpDate}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </section>
);

export default ImpactTracker;
