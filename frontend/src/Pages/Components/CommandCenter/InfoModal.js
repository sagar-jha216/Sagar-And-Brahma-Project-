import React from 'react';
import imgR from '../../../assets/CommandCenterImage/Group 156619.svg';
import imgInfo from '../../../assets/CommandCenterImage/Path 50602.png';
import action from '../../../assets/CommandCenterImage/Group 156595.svg';

const InfoModal = ({ isOpen, onClose, modalData }) => {
  if (!isOpen || !modalData) return null;

  return (
    <div style={{font: "normal normal Funnel Sans",paddingLeft: "100px"}}>
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 text-left">
      <div className="bg-white rounded-lg shadow-xl max-w-[1100px] max-h-[550px] w-full mx-4 flex flex-col">
        {/* Header - Fixed */}
        <div className="flex items-center justify-between px-6 py-2 border-b border-gray-200 flex-shrink-0">
          <h2 className="text-lg font-bold text-gray-900">{modalData.title}</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl font-light"
          >
            ×
          </button>
        </div>

        {/* Content - Scrollable */}
        <div className="p-6 space-y-4 overflow-y-auto flex-1 max-h-[660px]">        
          {modalData.issues.map((issue, issueIndex) => (
            <div key={issue.id} className="bg-[#F4F2F2] rounded-lg p-8">
              {/* First Row - Issue Description with Green Box */}
              <div className="flex gap-4 mb-4">
                {/* Left Column - 85% width - Issue Description */}
                <div className="w-[85%]">
                  <div className="flex items-center space-x-2">
                     <img src={imgInfo} alt="" className="h-4 w-4 mb-2" style={{marginLeft:"-24px"}} />
                    <h3 className="text-[18px] font-bold text-gray-900 mb-2">{issue.title}</h3>
                  </div>
                  <div className="space-y-1 text-xs text-gray-700">
                    {issue.description.map((desc, descIndex) => (
                      <div className='text-[12px] ' key={descIndex}><span className='text-[12px] font-bold'>{desc.title}</span> <span className='font-extralight'> {desc.info}</span> </div>
                    ))}
                  </div>
                </div>
                
                {/* Right Column - 15% width - Green Box */}
                <div className="w-[15%] flex items-start justify-end">
                  <div className="border-2 border-dashed bg-white border-green-400 px-3 py-2 rounded">
                    <div className="text-xs font-medium text-black">Potential</div>
                    <div className="text-xs font-medium text-black">Loss Mitigation:</div>
                    <div className="text-sm font-bold text-black">{issue.potentialLossMitigation}</div>
                  </div>
                </div>
              </div>

              {/* Second Row - Remediation Full Width */}
              <div className="w-full">
                <div className="flex items-center space-x-2 mb-2 ">
                  {/* <div className="w-4 h-4 rounded flex items-center justify-center">
                    <span className="text-white text-xs"  > */}
                       <img src={imgR} alt="img" className="h-5 w-5 mb-2" style={{marginLeft:"-24px"}} />
                       {/* </span>
                  </div> */}
                  <h4 className="text-[18px] font-bold text-gray-900" style={{marginLeft:"4px"}}>Remediation</h4>
                </div>

                {/* Remediation Items */}
                <div className="space-y-2">
                  {issue.remediation.map((remedy, remedyIndex) => (
                    <div key={remedy.id} className="bg-white rounded-lg p-3 shadow-sm flex items-center">
                      <div className="flex items-center space-x-3 w-[40%] lg:w-[50%]">
                        <div className="w-6 h-6 bg-yellow-100 rounded-full flex items-center justify-center flex-shrink-0">
                          <span className="text-yellow-600 font-bold text-xs">{remedy.id}</span>
                        </div>
                        <div className="min-w-0">
                          <div className="text-xs font-base text-black font-light">{remedy.title}</div>
                          {remedy.subtitle && (
                            <div className="text-xs font-base text-black font-light">{remedy.subtitle}</div>
                          )}
                        </div>
                      </div>
                      <div className="text-left w-[18%] lg:w-[15%] flex-shrink-0">
                        <div className="text-[12px] font-semibold text-[#6d706b]">Gross Margin % :</div>
                        <div className={`text-sm font-bold ${
                          remedy.marginVariance.includes('-') ? 'text-red-600' : 'text-green-600'
                        }`}>{remedy.marginVariance}</div>
                      </div>
                      <div className="text-left w-[18%] lg:w-[20%] flex-shrink-0">
                        <div className="text-[12px] font-semibold text-[#6d706b]">Loss Mitigation</div>
                        <div className="text-sm font-bold text-gray-900">{remedy.lossMitigation}</div>
                      </div>
                      <div className="w-[24%] lg:w-[20%] flex justify-end">
                        <button
                          style={{ background: "#FFF2DF" }}
                          className="flex items-center space-x-2 text-xs font-bold text-gray-900 rounded py-1 px-1"
                        >
                          <div className="w-6 h-6 flex justify-center">
                            <span className="text-white text-xs"><img src={action} alt="" className="h-5 w-5 mb-2" /></span>
                          </div>
                          <span>Action</span>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
    </div>
  );
};

export default InfoModal;
