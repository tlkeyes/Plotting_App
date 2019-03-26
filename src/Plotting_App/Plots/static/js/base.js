endpoint = 'api/chart/data'
    $.ajax({

        method: "GET",
        url : endpoint,
        success: function(data){
            date = data.date
            uHat = data.u_hat
            rate = data.rate
            warning = data.warning
            upper = data.upper
            setChart('uChart')
            unitTypeChart('unitType1')
            unitTypeChart('unitType2')
            unitTypeChart('unitType3')
            unitTypeChart('unitType4')
            setChart2()
            setChart3()
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
    function unitTypeChart(chartName){
      new Chart(document.getElementById(chartName), {
        type: 'line',
        data: {
          labels: date,
          datasets: [{
            label: chartName,
            data: rate,
            tension: 0,
            backgroundColor: 'rgba(0,123,255,0.1)',
            borderColor: 'rgba(0,123,255,1)',
            pointBackgroundColor: '#ffffff',
            pointHoverBackgroundColor: 'rgb(0,123,255)',
            borderWidth: 2,
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

    function setChart2(){
      new Chart(document.getElementById("doughnut-chart"), {
      type: 'doughnut',
      data: {
        labels: ["Unit1", "Unit2", "Unit3", "Unit4", "Unit5"],
        datasets: [
          {
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
            data: [2478,5267,734,784,433]
          }
        ]
      },
      options: {
        title: {
          display: false,
          text: "Patient Days Across All Unit Types"
          }
        }
      })
    }

    function setChart3(){
        new Chart(document.getElementById("bar-chart"), {
        type: 'horizontalBar',
        data: {
            labels: ["Unit1", "Unit2", "Unit3", "Unit4", "Unit5"],
            datasets: [
                {
                    label: "stuff",
                    backgroundColor: "#3e95cd",
                    data: [2478,5267,734,784,433]
                }
            ]
        },
        options: {
            title: {
                display: false,
                text: "Some other metric"
            }
        }
        })
    }