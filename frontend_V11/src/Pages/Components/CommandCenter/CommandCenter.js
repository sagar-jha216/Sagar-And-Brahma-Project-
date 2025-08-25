import React, { useEffect, useState } from 'react';
import InfoModal from './InfoModal';

import img3 from '../../../assets/CommandCenterImage/info-icon.svg';
import img4 from '../../../assets/CommandCenterImage/Path 61.svg';
import img5 from '../../../assets/CommandCenterImage/Path 63.png';
import img6 from '../../../assets/CommandCenterImage/Path 19.svg';
import img7 from '../../../assets/CommandCenterImage/Group 2.svg';
import img8 from '../../../assets/CommandCenterImage/Group 156818.svg';
import img9 from '../../../assets/CommandCenterImage/Path 109.svg';
import img10 from '../../../assets/CommandCenterImage/Path 50602.png';
import img11 from '../../../assets/CommandCenterImage/Path 50481.svg';

import i864 from '../../../assets/CommandCenterImage/Group 156864.png';
import i865 from '../../../assets/CommandCenterImage/Group 156865.png';
import i866 from '../../../assets/CommandCenterImage/Group 156866.png';
import i867 from '../../../assets/CommandCenterImage/Group 156867.png';
import i868 from '../../../assets/CommandCenterImage/Group 156868.svg';
import i870 from '../../../assets/CommandCenterImage/Group 156870.png';
import i871 from '../../../assets/CommandCenterImage/Group 156871.png';
import i872 from '../../../assets/CommandCenterImage/Group 156872.png';

import { Filters } from "./Filters";

const images=[i864,i865,i866,i867,i868,i870,i871,i872];

const parseCurrency = (s) => {
  if (!s) return 0;
  const num = parseFloat(String(s).replace(/[^0-9.-]+/g,""));
  return isNaN(num) ? 0 : num;
};
const formatCurrency = (n) => {
  if (n == null) return "$0";
  return "$" + Number(n).toLocaleString();
};

const CommandCenter = () => {
  const [rawData, setRawData] = useState(null); // full json
  const [dashboardData, setDashboardData] = useState(null); // currently displayed region object
  const [pendingFilters, setPendingFilters] = useState(null);

  // Fetch data.json (public/data/data.json)
  useEffect(() => {
    fetch('/data/data.json')
      .then(response => response.json())
      .then(data => {
        setRawData(data);
        // default: Global
        if (data && data.Global) {
          setDashboardData(data.Global);
        } else {
          // fallback first key
          const firstKey = Object.keys(data || {})[0];
          if (firstKey) setDashboardData(data[firstKey]);
        }

        // if filters awaited, apply them
        if (pendingFilters) {
          applyFiltersToData(data, pendingFilters);
          setPendingFilters(null);
        }
      })
      .catch(error => {
        console.error("Error fetching data.json", error);
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // modal states
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedProcess, setSelectedProcess] = useState(null);
  const [selectedModalData, setSelectedModalData] = useState(null);

  // helper: apply filter object to raw data and set dashboardData
  const applyFiltersToData = (raw, filters) => {
    if (!raw) return;
    const regionKey = filters.region || "Global";
    const regionObj = raw[regionKey] || raw["Global"] || raw[Object.keys(raw)[0]];
    if (!regionObj) {
      setDashboardData(null);
      return;
    }

    // compute multiplier (simple deterministic) based on number of selected filters
    const storeLen = (filters.selectedStores && filters.selectedStores.length) || 0;
    const channelLen = (filters.selectedChannels && filters.selectedChannels.length) || 0;
    const totalFilters = storeLen + channelLen;
    // each filter reduces visible totals by 12% (example) but don't go below 20%
    let multiplier = 1;
    if (totalFilters > 0) {
      multiplier = Math.max(0.2, 1 - totalFilters * 0.12);
    }

    // deep clone regionObj (shallow enough)
    const newRegion = JSON.parse(JSON.stringify(regionObj));

    // adjust shrinkImpactValues totals
    const baseTotal = parseCurrency(regionObj.shrinkImpactValues?.totalShrink);
    newRegion.shrinkImpactValues = newRegion.shrinkImpactValues || {};
    newRegion.shrinkImpactValues.totalShrink = formatCurrency(Math.round(baseTotal * multiplier));

    // adjust shrinkHotspots values
    if (Array.isArray(newRegion.shrinkHotspots)) {
      newRegion.shrinkHotspots = newRegion.shrinkHotspots.map(h => {
        const amt = parseCurrency(h.amount);
        return { ...h, amount: formatCurrency(Math.round(amt * multiplier)) };
      });
    }

    // adjust root causes
    if (Array.isArray(newRegion.rootCauses)) {
      newRegion.rootCauses = newRegion.rootCauses.map(r => {
        const amt = parseCurrency(r.impact);
        return { ...r, impact: formatCurrency(Math.round(amt * multiplier)) };
      });
    }

    // adjust quick actions labels slightly to indicate filtered
    if (Array.isArray(newRegion.quickActions)) {
      newRegion.quickActions = newRegion.quickActions.map((q, idx) => ({
        ...q,
        title: totalFilters > 0 ? `${q.title} (filtered)` : q.title
      }));
    }

    // adjust processData counts but KEEP all 8 items (titles same)
    if (Array.isArray(newRegion.processData)) {
      newRegion.processData = newRegion.processData.map(proc => {
        const baseErr = proc.errorCount || 0;
        const baseSuc = proc.successCount || 0;
        // Simple deterministic change:
        const newErr = Math.round(baseErr * multiplier);
        const newSuc = Math.round(baseSuc * multiplier);
        return { ...proc, errorCount: newErr, successCount: newSuc };
      });
    }

    // modal data remains same (so modal shows details per process)
    setDashboardData(newRegion);
  };

  // parent will call this when Filters change (auto or Apply)
  const handleApplyFilters = (selectedFilters) => {
    // if rawData not loaded yet, store pending filters
    if (!rawData) {
      setPendingFilters(selectedFilters);
      return;
    }
    applyFiltersToData(rawData, selectedFilters);
  };

  // clicking on left item should open modal (if it has issues)
  const handleInfoClick = (processItem) => {
    setSelectedProcess(processItem);

    // modalDataByProcess exists in dashboardData (region-wise)
    const modalData = dashboardData?.modalDataByProcess?.[processItem.title];
    setSelectedModalData(modalData || null);
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedProcess(null);
    setSelectedModalData(null);
  };

  return (
    <div style={{ font: "normal normal bold 16px/20px Funnel Sans" }}>

      <div className="w-full bg-gray-200">

        <div className="w-full h-[687px] bg-gray-100 overflow-hidden shadow-lg rounded">
          {/* Filters */}
          <Filters onApply={handleApplyFilters} />
          <div className="h-[687px] px-2 sm:px-4 overflow-x-hidden overflow-y-auto lg:overflow-hidden">
            {/* Alert Banner */}
            <div className="bg-[#fff3df] h-[30px] px-2 sm:px-4 flex items-center mb-3 shadow-[0_2px_4px_0_rgba(0,0,0,0.1)]">
              <img src={img3} alt="info-icon" className="inline-block h-3.5 w-3.5 mr-1" />
              <p className="text-[#282a27] text-sm truncate font-extralight ">
                Mars is undercutting prices in Frozen desserts and ice cream by 4% ; Sales down in Frozen Vegetables & Fruits by 6% Eggo Homestyle Waffles (10 ct) is the new top selling SKU
              </p>
            </div>

            {/* Content Area */}
            <div className="flex flex-col lg:flex-row gap-2 lg:gap-4 lg:h-full text-left">
              {/* Left Panel */}
              <div className="w-full lg:w-5/12 space-y-[6px]">
                {dashboardData?.processData?.map((item, index) => (
                  <div
                    key={index}
                    className={`bg-white rounded h-[63px] shadow-sm px-3 sm:px-6 flex items-center justify-between ${item.errorCount > 0 ? 'cursor-pointer hover:bg-gray-50 transition-colors' : ''
                      }`}
                    onClick={item.errorCount > 0 ? () => handleInfoClick(item) : undefined}
                  >
                    <div className="flex items-center space-x-2 sm:space-x-4 flex-1 min-w-0">
                      <div className="w-[35px] h-[35px] sm:w-[43px] sm:h-[43px] bg-[#FFE6C2] rounded-full flex items-center justify-center flex-shrink-0">
                        <img src={images[index]} alt="icon" className="w-10 h-10" />
                      </div>
                      <span className="text-sm sm:text-[14px] text-[#282a27] font-bold truncate">{item.title}</span>
                    </div>
                    <div className="flex items-center space-x-2 sm:space-x-4 flex-shrink-0">
                      <div className="flex items-center space-x-1 sm:space-x-2">
                        <img src={img4} alt="" className="w-4 h-4" />
                        <span className="text-sm text-black">{item.errorCount}</span>
                      </div>

                      <div className="h-4 border-l-[2px] border-gray-300"></div>

                      <div className="flex items-center space-x-1 sm:space-x-2">
                        <img src={img5} alt="" className="w-4 h-4" />
                        <span className="text-sm text-black">{item.successCount}</span>
                      </div>

                    </div>
                  </div>
                ))}
              </div>

              {/* Center Panel */}
              <div className="w-full lg:w-3/12 space-y-5">
                <div className="bg-white rounded-lg h-[327px] shadow-sm p-4">
                  <div className="h-[112px] bg-green-200 rounded relative mb-3">
                    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3887.657216513695!2d77.60495755000001!3d12.971598550000011!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae1670c9b44e6d%3A0xf8dfc3ed25e46ba1!2sBangalore%2C%20Karnataka%2C%20India!5e0!3m2!1sen!2sin!4v1664801416449!5m2!1sen!2sin" width="100%" height="100%" style={{ border: 0 }} allowFullScreen="" loading="lazy" referrerPolicy="no-referrer-when-downgrade"></iframe>
                  </div>

                  <div>
                    <h3 className="font-bold text-[14px] mb-2 text-black">Shrink Loss Hotspots - Top 3 Stores</h3>
                    <div className="h-px bg-yellow-400 mb-3"></div>
                    <div className="space-y-3">
                      {dashboardData?.shrinkHotspots?.map((hotspot, index) => (
                        <div key={index} className="flex items-start space-x-2">
                          <img src={img6} alt="info" className="w-4 h-4" />
                          <div className="flex-1">
                            <div className="text-xs mb-1 font-extralight text-black">{hotspot.name}</div>
                            <div className="text-xs font-bold text-black">{hotspot.amount}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg h-[200px] shadow-sm p-4">
                  <h3 className="font-bold text-[14px] mb-2 text-black">Top 3 Root Causes by $ Impact</h3>
                  <div className="h-px bg-yellow-400 mb-3"></div>
                  <div className="space-y-3">
                    {dashboardData?.rootCauses?.map((rootCause, index) => (
                      <div key={index} className="flex items-start space-x-2">
                        <img src={img7} alt="info" className="w-3 h-3" />
                        <div className="flex-1">
                          <div className="text-xs mb-1 text-black font-extralight">{rootCause.cause}</div>
                          <div className="text-xs font-bold text-black">{rootCause.impact}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Right Panel */}
              <div className="w-full lg:w-4/12 space-y-5">
                <div className="bg-white rounded-lg h-[155px] shadow-sm p-4">
                  <h3 className="font-bold text-[14px] mb-3 text-black">Total Shrink Impact (Real-time $ + Trend)</h3>
                  <div className="grid grid-cols-3 gap-2">
                    <div className="bg-[#F4F2F2] rounded p-2 flex flex-col justify-between h-[90px]">
                      <div className="text-[12px] text-[#282a27]">Total Known Shrink Identified ($)</div>
                      <div className="text-[14px] font-bold text-black">{dashboardData?.shrinkImpactValues?.totalShrink}</div>
                    </div>
                    <div className="bg-[#F4F2F2] rounded p-2 flex flex-col justify-between h-[90px]">
                      <div className="text-[12px] text-[#282a27]">Shrink % of <br/> Sales</div>
                      <div className="flex justify-between ">
                        <div className="text-black flex justify-between items-end text-[13px]">{dashboardData?.shrinkImpactValues?.shrinkPercent}</div>
                        <div className=" text-white flex justify-between "><img src={img8} alt="info" className="w-10 h-10" /></div>
                      </div>
                    </div>
                    <div className="bg-[#F4F2F2] rounded p-2 flex flex-col justify-between h-[90px]">
                      <div className="text-[12px] text-[#282a27]">Top Shrink Driver</div>
                      <div className="flex flex-col">
                        <div className="text-[11px] text-black font-extralight flex flew-row mt- -3 gap-1">
                          <span><img src={img9} className="w-4 h-4" alt=""/> </span>
                          {dashboardData?.shrinkImpactValues?.topDriver}
                        </div>
                        <div className="text-[11px] font-bold text-black">{dashboardData?.shrinkImpactValues?.driverPercent}</div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg h-[374px] shadow-sm p-4">
                  <h3 className="font-bold text-sm mb-3 text-black text-[14px]">Quick Actions</h3>
                  <div className="space-y-4">
                    {dashboardData?.quickActions?.map((action, index) => (
                      <div key={index} className="bg-[#F4F2F2] rounded p-2.5">
                        <div className="flex items-start space-x-2">
                          <div className="w-4 h-4 rounded-full mt-0.5 flex-shrink-0">
                            <img src={img10} alt="" />
                          </div>
                          <div className="flex-1">
                            <div className="text-[13px] text-left font-medium mb-2 text-black">{action.title}</div>
                            <div className="h-px bg-gray-300 mb-2"></div>
                            <div className="flex items-center justify-between">
                              <span className="text-[11px] text-black font-extralight">{action.location}</span>
                              <button className="bg-black text-white text-xs px-3 py-1 rounded-xl flex items-center space-x-1 font-extralight">
                                <span>Action</span>
                                <img src={img11} alt="" className="w-3 h-3" />
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

        <InfoModal
          isOpen={isModalOpen}
          onClose={handleModalClose}
          data={selectedProcess}
          modalData={selectedModalData}
        />
      </div>
    </div>
  );
};

export default CommandCenter;
