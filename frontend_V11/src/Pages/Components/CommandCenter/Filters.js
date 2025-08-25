import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "./Filters.css";
import "./CustomDatePicker.css";
import { useHistory } from 'react-router-dom';

import backIcon from '../../../assets/CommandCenterImage/Group 156425.svg';
import filtericon from '../../../assets/CommandCenterImage/Path 50349.svg';
import navarrowicon from '../../../assets/CommandCenterImage/nav-arrow-icon.svg';

const demoData = {
  regions: ["Global", "South", "East", "West"],
  stores: {
    Global: ["Store #1001 - NY", "Store #1002 - NJ"],
    South: ["Store #2001 - TX", "Store #2002 - FL"],
    East: ["Store #3001 - MA", "Store #3002 - CT"],
    West: ["Store #4001 - CA", "Store #4002 - WA"],
  },
  channels: ["E-commerce", "Wholesale", "Retail", "Direct", "Franchise"],
};

export const Filters = ({ onApply }) => {
  const history = useHistory();
  const [region, setRegion] = useState(demoData.regions[0]);
  const [hoveredRegion, setHoveredRegion] = useState(null);
  const [isTimePeriodOpen, setIsTimePeriodOpen] = useState(false);

  const [selectedStores, setSelectedStores] = useState([]);
  const [selectedChannels, setSelectedChannels] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);

  // reset stores when region changes
  useEffect(() => {
    setSelectedStores([]);
  }, [region]);

  // AUTO APPLY: whenever any filter changes, call onApply immediately
  useEffect(() => {
    if (typeof onApply === "function") {
      onApply({
        region,
        selectedStores,
        selectedChannels,
        selectedDate
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [region, selectedStores, selectedChannels, selectedDate]);

  const toggleCheckbox = (value, currentValues, setter) => {
    if (currentValues.includes(value)) {
      setter(currentValues.filter((v) => v !== value));
    } else {
      setter([...currentValues, value]);
    }
  };

  return (
    <div className="pb-4">
      <div className="filter-bar">
        <div className="flex items-center space-x-2">
          <button className="arrow-btn">
            <img src={backIcon} alt="Back"  onClick={() => history.push('/Home')}/>
          </button>
        </div>

        <div className="flex items-center space-x-2 flex-wrap">
          <img
            src={filtericon}
            alt="filter-icon"
            className="filter-bar-icon"
          />
          <Dropdown label="Region" hoverHighlight selectedValue={region}>
            {demoData.regions.map((r) => {
              const isSelected = region === r;
              const isHovered = hoveredRegion === r;

              const shouldHighlightOrange =
                isHovered || (!hoveredRegion && isSelected);

              return (
                <div
                  key={r}
                  className={`region-option px-3 py-1 text-xs cursor-pointer rounded ${
                    shouldHighlightOrange ? "text-orange-500" : "text-white"
                  }`}
                  onClick={() => setRegion(r)}
                  onMouseEnter={() => setHoveredRegion(r)}
                  onMouseLeave={() => setHoveredRegion(null)}
                >
                  {r}
                </div>
              );
            })}
          </Dropdown>

          {/* Store Dropdown */}
          <Dropdown
            label="Store"
            selectedValue={
              selectedStores.length
                ? selectedStores.length === 1
                  ? selectedStores[0]
                  : `${selectedStores.length} selected`
                : "Store"
            }
          >
            {demoData.stores[region].map((store) => (
              <div key={store} className="dropdown-option">
                <input
                  type="checkbox"
                  checked={selectedStores.includes(store)}
                  onChange={() =>
                    toggleCheckbox(store, selectedStores, setSelectedStores)
                  }
                />
                <span>{store}</span>
              </div>
            ))}
          </Dropdown>

          {/* Time Period */}
          <Dropdown
            label="Time Period"
            selectedValue={
              selectedDate ? selectedDate.toLocaleDateString() : "Time Period"
            }
            isCalendar
          >
            <div className="calendar-container">
              <DatePicker
                selected={selectedDate}
                onChange={(date) => setSelectedDate(date)}
                inline
                calendarClassName="custom-datepicker"
                showPopperArrow={false}
                dayClassName={(date) =>
                  date.getMonth() !== (selectedDate || new Date()).getMonth()
                    ? "faded-day"
                    : undefined
                }
              />
            </div>
          </Dropdown>

          {/* Store Channel */}
          <Dropdown
            label="Store Channel"
            selectedValue={
              selectedChannels.length
                ? selectedChannels.length === 1
                  ? selectedChannels[0]
                  : `${selectedChannels.length} selected`
                : "Store Channel"
            }
          >
            {demoData.channels.map((channel) => (
              <div key={channel} className="dropdown-option">
                <input
                  type="checkbox"
                  checked={selectedChannels.includes(channel)}
                  onChange={() =>
                    toggleCheckbox(
                      channel,
                      selectedChannels,
                      setSelectedChannels
                    )
                  }
                />
                <span>{channel}</span>
              </div>
            ))}
          </Dropdown>

          {/* Apply/Clear Buttons */}
          <div className="flex space-x-2 ml-2">
            
            {/*<button
              className="btn-apply"
              onClick={() => {
                if (typeof onApply === "function") {
                  onApply({
                    region,
                    selectedStores,
                    selectedChannels,
                    selectedDate
                  });
                }
              }}
            >
              Apply
            </button>*/}

            <button
              className="btn-clear"
              onClick={() => {
                setRegion(demoData.regions[0]);
                setSelectedStores([]);
                setSelectedChannels([]);
                setSelectedDate(null);
              }}
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const Dropdown = ({
  label,
  children,
  selectedValue,
  hoverHighlight = false,
  isCalendar = false,
}) => (
  <div className="dropdown group relative">
    <button className="dropdown-button">
      <span className="dropdown-label mr-3">{selectedValue || label}</span>

      <span className="dropdown-arrow group-hover:rotate-180">
        <img src={navarrowicon} alt="arrow-icon" />
      </span>
    </button>
    <div
      className={`dropdown-menu ${isCalendar ? "dropdown-menu-calendar" : ""}`}
    >
      <div
        className={`dropdown-content ${
          hoverHighlight ? "region-highlight" : ""
        }`}
      >
        {children}
      </div>
    </div>
  </div>
);
