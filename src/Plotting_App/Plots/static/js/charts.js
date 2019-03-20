var bouCtx = document.getElementsByClassName('blog-overview-users')[0];

// Data
var bouData = {
  // Generate the days labels on the X axis.
  labels: Array.from(new Array(30), function (_, i) {
    return i === 0 ? 1 : i;
  }),
  labels: date,
  datasets: [{
    label: 'Rate',
    fill: 'start',
    data: rate,
    backgroundColor: 'rgba(0,123,255,0.1)',
    borderColor: 'rgba(0,123,255,1)',
    pointBackgroundColor: '#ffffff',
    pointHoverBackgroundColor: 'rgb(0,123,255)',
    borderWidth: 1.5,
    pointRadius: 0,
    pointHoverRadius: 3
  }, 
//   {
//     label: 'Past Month',
//     fill: 'start',
//     data: [380, 430, 120, 230, 410, 740, 472, 219, 391, 229, 400, 203, 301, 380, 291, 620, 700, 300, 630, 402, 320, 380, 289, 410, 300, 530, 630, 720, 780, 1200],
//     backgroundColor: 'rgba(255,65,105,0.1)',
//     borderColor: 'rgba(255,65,105,1)',
//     pointBackgroundColor: '#ffffff',
//     pointHoverBackgroundColor: 'rgba(255,65,105,1)',
//     borderDash: [3, 3],
//     borderWidth: 1,
//     pointRadius: 0,
//     pointHoverRadius: 2,
//     pointBorderColor: 'rgba(255,65,105,1)'
//   }
]
};

// Options
var bouOptions = {
  responsive: true,
  legend: {
    position: 'top'
  },
  elements: {
    line: {
      // A higher value makes the line look skewed at this ratio.
      tension: 0.3
    },
    point: {
      radius: 0
    }
  },
  scales: {
    xAxes: [{
      gridLines: false,
      ticks: {
        callback: function (tick, index) {
          // Jump every 7 values on the X axis labels to avoid clutter.
          return index % 7 !== 0 ? '' : tick;
        }
      }
    }],
    yAxes: [{
      ticks: {
        suggestedMax: 45,
        callback: function (tick, index, ticks) {
          if (tick === 0) {
            return tick;
          }
          // Format the amounts using Ks for thousands.
          return tick > 999 ? (tick/ 1000).toFixed(1) + 'K' : tick;
        }
      }
    }]
  },
  // Uncomment the next lines in order to disable the animations.
  // animation: {
  //   duration: 0
  // },
  hover: {
    mode: 'nearest',
    intersect: false
  },
  tooltips: {
    custom: false,
    mode: 'nearest',
    intersect: false
  }
};

// Generate the Analytics Overview chart.
window.BlogOverviewUsers = new Chart(bouCtx, {
  type: 'LineWithLine',
  data: bouData,
  options: bouOptions
});