
import {useState,useEffect} from "react";
import LeaderDashboardCard from './LeaderDashboardCard';
import { RetailLeaderBoardData } from '../../../../Data/mockData';

const RetailLeaderBoard = () => {

  return (
    <div className="min-h-screen bg-soft">
      <div className="max-w-md mx-auto">
        <LeaderDashboardCard data={RetailLeaderBoardData} />
      </div>
    </div>
  );
};

export default RetailLeaderBoard;

