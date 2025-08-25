

export const impactData = {
  summary: {
    todaysLossMitigation: 9000,
    todaysLossMitigationComparison: {
      percentage: 4.8,
      trendDirection: "up",
      compareTo: "LD",
    },

    monthToDateLossMitigation: 29900,
    monthToDateLossMitigationComparison: {
      percentage: 3.2,
      trendDirection: "up",
      compareTo: "LM",
    },

    yearToDateLossMitigation: 118000,
    yearToDateLossMitigationComparison: {
      percentage: 1.1,
      trendDirection: "down",
      compareTo: "LY",
    },

    shrinkageAlertsTriggered: 3,
    avgTimeForResolution: 14,
    incidentFrequency: 2,
  },

  last7DaysLossMitigation: [
    { date: "01-Jul", value: 9000 },
    { date: "02-Jul", value: 5000 },
    { date: "03-Jul", value: 10000 },
    { date: "04-Jul", value: 6000 },
    { date: "05-Jul", value: 8000 },
    { date: "06-Jul", value: 2000 },
    { date: "07-Jul", value: 4000 },
  ],

  monthlyLossMitigationPerStore: [
    { store: "2145-NY", value: 5000 },
    { store: "5360-PA", value: 4500 },
    { store: "5360-PA", value: 4300 },
    { store: "8243-NY", value: 4000 },
    { store: "3682-CT", value: 3500 },
    { store: "3296-L", value: 3000 },
    { store: "5931-MN", value: 2600 },
    { store: "1092-OH", value: 2000 },
    { store: "4710-WI", value: 1000 },
  ],

  weeklyShrinkReport: [
    {
      date: "01/07/25",
      store: "Store #329",
      shrinkageType: "Lower Sell Through Rate",
      estimatedLoss: 2300,
      rootCause: "Poor Product Assortment",
      actionTaken: "Reallocation to a store with high Sell Through Rate",
      impactScore: 4,
      followUpDate: "15/07/25",
    },
    {
      date: "02/07/25",
      store: "Store #593",
      shrinkageType: "Product (Inventory) Returned by Customer",
      estimatedLoss: 800,
      rootCause: "Return by Customer due to poor packaging",
      actionTaken: "Donate to a nearby Homeless Center",
      impactScore: 3,
      followUpDate: "10/07/25",
    },
    {
      date: "03/07/25",
      store: "Store #109",
      shrinkageType: "Seasonal Overstock",
      estimatedLoss: 2300,
      rootCause: "Delayed Store Replenishment",
      actionTaken: "Liquidate the inventory via a third party approved Liquidator",
      impactScore: 4,
      followUpDate: "05/07/25",
    },
  ],
};



export const southData = {
  summary: {
    todaysLossMitigation: 4800,
    todaysLossMitigationComparison: {
      percentage: -2.5,
      trendDirection: "down",
      compareTo: "LD",
    },

    monthToDateLossMitigation: 15200,
    monthToDateLossMitigationComparison: {
      percentage: 1.7,
      trendDirection: "up",
      compareTo: "LM",
    },

    yearToDateLossMitigation: 80500,
    yearToDateLossMitigationComparison: {
      percentage: 0.8,
      trendDirection: "down",
      compareTo: "LY",
    },

    shrinkageAlertsTriggered: 6,
    avgTimeForResolution: 11,
    incidentFrequency: 3,
  },

  last7DaysLossMitigation: [
    { date: "01-Jul", value: 2200 },
    { date: "02-Jul", value: 1800 },
    { date: "03-Jul", value: 2400 },
    { date: "04-Jul", value: 1600 },
    { date: "05-Jul", value: 1900 },
    { date: "06-Jul", value: 1200 },
    { date: "07-Jul", value: 1300 },
  ],

  monthlyLossMitigationPerStore: [
    { store: "3421-TX", value: 4200 },
    { store: "7810-FL", value: 3700 },
    { store: "9210-GA", value: 3200 },
    { store: "6621-AL", value: 2500 },
    { store: "1198-TN", value: 1800 },
  ],

  weeklyShrinkReport: [
    {
      date: "01/07/25",
      store: "Store #2001 - TX",
      shrinkageType: "Theft",
      estimatedLoss: 1800,
      rootCause: "Internal Theft",
      actionTaken: "Employee terminated and legal action taken",
      impactScore: 5,
      followUpDate: "15/07/25",
    },
    {
      date: "03/07/25",
      store: "Store #2002 - FL",
      shrinkageType: "Expired Goods",
      estimatedLoss: 1200,
      rootCause: "Slow Inventory Turnover",
      actionTaken: "Promotional push to accelerate sales",
      impactScore: 3,
      followUpDate: "20/07/25",
    },
  ],
};


export const eastData = {
  summary: {
    todaysLossMitigation: 6200,
    todaysLossMitigationComparison: {
      percentage: 5.0,
      trendDirection: "up",
      compareTo: "LD",
    },

    monthToDateLossMitigation: 21400,
    monthToDateLossMitigationComparison: {
      percentage: 3.2,
      trendDirection: "up",
      compareTo: "LM",
    },

    yearToDateLossMitigation: 99500,
    yearToDateLossMitigationComparison: {
      percentage: -1.1,
      trendDirection: "down",
      compareTo: "LY",
    },

    shrinkageAlertsTriggered: 4,
    avgTimeForResolution: 9,
    incidentFrequency: 2,
  },

  last7DaysLossMitigation: [
    { date: "01-Jul", value: 2500 },
    { date: "02-Jul", value: 3000 },
    { date: "03-Jul", value: 1500 },
    { date: "04-Jul", value: 1800 },
    { date: "05-Jul", value: 2100 },
    { date: "06-Jul", value: 2600 },
    { date: "07-Jul", value: 2000 },
  ],

  monthlyLossMitigationPerStore: [
    { store: "3242-MA", value: 4300 },
    { store: "5543-CT", value: 3800 },
    { store: "1119-PA", value: 3600 },
    { store: "7777-NJ", value: 3000 },
    { store: "8910-NY", value: 2500 },
  ],

  weeklyShrinkReport: [
    {
      date: "02/07/25",
      store: "Store #3001 - MA",
      shrinkageType: "Damaged Packaging",
      estimatedLoss: 1100,
      rootCause: "Rough handling in storage",
      actionTaken: "Retrained staff on proper handling",
      impactScore: 2,
      followUpDate: "12/07/25",
    },
    {
      date: "04/07/25",
      store: "Store #3002 - CT",
      shrinkageType: "Shoplifting",
      estimatedLoss: 1700,
      rootCause: "Insufficient floor staff",
      actionTaken: "Increased staff presence and CCTV",
      impactScore: 4,
      followUpDate: "18/07/25",
    },
  ],
};


export const westData = {
  summary: {
    todaysLossMitigation: 7100,
    todaysLossMitigationComparison: {
      percentage: 8.1,
      trendDirection: "up",
      compareTo: "LD",
    },

    monthToDateLossMitigation: 19800,
    monthToDateLossMitigationComparison: {
      percentage: -2.5,
      trendDirection: "down",
      compareTo: "LM",
    },

    yearToDateLossMitigation: 87000,
    yearToDateLossMitigationComparison: {
      percentage: 4.0,
      trendDirection: "up",
      compareTo: "LY",
    },

    shrinkageAlertsTriggered: 7,
    avgTimeForResolution: 13,
    incidentFrequency: 4,
  },

  last7DaysLossMitigation: [
    { date: "01-Jul", value: 2800 },
    { date: "02-Jul", value: 3100 },
    { date: "03-Jul", value: 2700 },
    { date: "04-Jul", value: 2600 },
    { date: "05-Jul", value: 3000 },
    { date: "06-Jul", value: 2300 },
    { date: "07-Jul", value: 2900 },
  ],

  monthlyLossMitigationPerStore: [
    { store: "4455-CA", value: 4700 },
    { store: "3322-WA", value: 4200 },
    { store: "9981-OR", value: 3500 },
    { store: "8880-NV", value: 2900 },
    { store: "1234-UT", value: 2100 },
  ],

  weeklyShrinkReport: [
    {
      date: "01/07/25",
      store: "Store #4001 - CA",
      shrinkageType: "Overstock",
      estimatedLoss: 1400,
      rootCause: "Poor demand forecasting",
      actionTaken: "Dynamic pricing and markdowns",
      impactScore: 3,
      followUpDate: "11/07/25",
    },
    {
      date: "05/07/25",
      store: "Store #4002 - WA",
      shrinkageType: "Fraudulent Returns",
      estimatedLoss: 1600,
      rootCause: "No return verification system",
      actionTaken: "Added return validation policy",
      impactScore: 4,
      followUpDate: "22/07/25",
    },
  ],
};
