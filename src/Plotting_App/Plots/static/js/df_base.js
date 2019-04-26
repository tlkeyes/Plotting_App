endpoint = 'api/chart/data/testdf'
    $.ajax({

        method: "GET",
        url : endpoint,
        success: function(data){
            console.log("Collected the data!!"),
            date = data.date
            rate = data.uchart.rate
            warning = data.uchart.warning
            upper = data.uchart.upper
            units = data.units
            unit_data = data.unit_data
            setChart('uChart')
            unitTypeCharts()
            unitScatterChart()
        }, 
        error: function(error_data){
            console.log("error"),
            console.log(error_data)
        }
    })

    function setChart(name){
        new Chart(document.getElementById(name), {
        type: 'line',
        data: {
            labels: date,
            datasets: [{
                label: 'Cauti Rate',
                data: rate,
                tension: 0,
                backgroundColor: 'rgba(0,123,255,0.1)',
                borderColor: 'rgba(0,123,255,1)',
                pointBackgroundColor: '#ffffff',
                pointHoverBackgroundColor: 'rgb(0,123,255)',
                borderWidth: 2,
                pointHoverRadius: 3,
                fill: false
                },
                {
                label: 'Warning',
                data: warning, 
                tension: 0,
                backgroundColor: 'rgba(255,215,0,0.1)',
                borderColor: 'rgba(255,215,0,1)',
                pointBackgroundColor: '#ffffff',
                pointHoverBackgroundColor: 'rgba(255,215,0,1)',
                borderDash: [3, 3],
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 2,
                pointBorderColor: 'rgba(255,215,0,1)',
                fill: '+1'
                },
                {
                label: 'Upper Bound',
                data: upper, 
                tension: 0,
                backgroundColor: 'rgba(255,65,105,0.1)',
                borderColor: 'rgba(255,65,105,1)',
                pointBackgroundColor: '#ffffff',
                pointHoverBackgroundColor: 'rgba(255,65,105,1)',
                borderDash: [3, 3],
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 2,
                pointBorderColor: 'rgba(255,65,105,1)',
                fill: 'end'
                }]
            },
        options: {
          scales: {
            xAxes: [{
              type: 'time',
              time: {
                unit: 'month',
                displayFormats: {
                  month: 'MMM YYYY'
                }
              }
            }]
          }
        }
      })
    }
    function unitTypeCharts(){
        for(let i = 0; i < units.length; i++){
            var unit_name = units[i];
            var rate_data = unit_data[unit_name].rate;

            new Chart(document.getElementById(unit_name), {
                type: 'line',
                data: {
                  labels: date,
                  datasets: [{
                    label: unit_name,
                    data: rate_data,
                    tension: 0,
                    backgroundColor: '#fafafa',
                    borderColor: 'rgba(0,123,255,1)',
                    pointBackgroundColor: '#ffffff',
                    pointHoverBackgroundColor: 'rgb(0,123,255)',
                    borderWidth: 2,
                    pointRadius: 0,
                    pointHoverRadius: 3,
                    fill: false
                    }]
                },
                options: {
                  scales: {
                    xAxes: [{
                      ticks: {
                        display: false
                      }
                    }]
                  }
                }
            })
        }
    }
    function unitScatterChart(){
      var data = [];
      var labels = []
      for(let i = 0; i < units.length; i++){
        var unit_name = units[i];
        var x = unit_data[unit_name].overall.denominator;
        var y = unit_data[unit_name].overall.rate;
        data.push({x: x, y: y})
        labels.push(unit_name)
      }
      console.log(data)
      new Chart(document.getElementById("unit-scatter-overall").getContext("2d"),{
        type: 'scatter',
        data: {
          labels: labels,
          datasets: [
            {
              data: data,
              backgroundColor: 'rgba(0,123,255,0.1)',
              borderColor: 'rgba(0,123,255,1)',
              pointBackgroundColor: '#ffffff',
              pointHoverBackgroundColor: 'rgb(0,123,255)',
              borderWidth: 2,
              pointHoverRadius: 3
            }
          ]
        },
        options: {
          scales: {
              xAxes: [{
                  type: 'linear',
                  position: 'bottom'
              }]
          },
          tooltips: {
            displayColors: false,
            callbacks: {
              title: function(tooltipItem, data) {
                return data['labels'][tooltipItem[0]['index']];
              }
            }
          }
        }
      })
    };