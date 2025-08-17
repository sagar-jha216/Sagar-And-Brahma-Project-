// import indicatorCatgoryPer from '../../../../assets/polygon-indicator.svg';

// const ProgressBar = ({ distribution, showLabels = false, ranges = null}) => {
//   const { green, yellow, red } = distribution;



//   return (
//     <div className="w-full">
//       {showLabels && ranges && (
//         <>
//           <div className="flex justify-between text-xs text-gray-500 mt-1">
//             <span>{ranges.low}</span>
//             <span>{ranges.medium}</span>
//             <span>{ranges.high}</span>
//           </div>
//           <img src={indicatorCatgoryPer} alt='Indicator' />
//         </>
//       )}
//       <div className="w-full bg-gray-200 rounded-full h-4">
//         <div className="flex h-4 rounded-full overflow-hidden">
//           <div
//             className="bg-success-green"
//             style={{ width: `${green}%` }}
//           ></div>
//           <div
//             className="bg-warning-yellow"
//             style={{ width: `${yellow}%` }}
//           ></div>
//           <div
//             className="bg-brand-red"
//             style={{ width: `${red}%` }}
//           ></div>


//         </div>


//       </div>

//     </div>
//   );
// };

// export default ProgressBar;







const ProgressBar = ({ distribution, showLabels = false, ranges = null, metric }) => {
  const { green, yellow, red } = distribution;


  return (
    <div className="w-full relative">
      {showLabels && ranges && (
        <>
          <div className="flex justify-between text-xs text-gray-500 mt-1 rangeSec">
            <span>{ranges.low}</span>
            <span>{ranges.medium}</span>
            <span>{ranges.high}</span>
          </div>


        </>
      )}

      <div className="w-full bg-gray-200 rounded-full h-4 relative">
        <div className="flex h-4 rounded-full overflow-hidden">
          <div className="bg-success-green" style={{ width: `${green}%` }}></div>
          <div className="bg-warning-yellow" style={{ width: `${yellow}%` }}></div>
          <div className="bg-brand-red" style={{ width: `${red}%` }}></div>
        </div>



      </div>
    </div>
  );
};
export default ProgressBar;
