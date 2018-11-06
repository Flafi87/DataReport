function loadJSON(callback) {   

    var xobj = new XMLHttpRequest();
        xobj.overrideMimeType("application/json");
    xobj.open('GET', 'data.json', true); // Replace 'my_data' with the path to your file
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
          }
    };
    xobj.send(null);  
 }
 function init() {
    loadJSON(function(response) {
     // Parse JSON string into object
       var actual_JSON = JSON.parse(response);
       console.log(actual_JSON)
       let my_time = Object.values(actual_JSON.Time);
       
       let my_sales = Object.values(actual_JSON.cumsum);
       function sortEggsInNest(a, b) {
        return a > b ? 1 : b > a ? -1 : 0;
      }
      my_sales = my_sales.sort(sortEggsInNest);
      my_time = my_time.sort(sortEggsInNest);
      my_time = my_time.map(x => (new Date(x).getTime()));
      let result = [];
      let target = [];
      const target_sales = 75000;
      ///
      for ( var i = 0; i < my_time.length; i++ ) {
        result.push( [ my_time[i], my_sales[i] ] );
        target.push( [ my_time[i], target_sales ])
      }

      ///

       var options = {
        chart: {
          type: 'line',
          animations: {
            enabled: true,
            easing: 'easeinout',
            speed: 800,
            animateGradually: {
                enabled: true,
                delay: 200
            },
            dynamicAnimation: {
                enabled: true,
                speed: 800
            }
        }
        },
        dataLabels: {
            enabled: false
          },
          stroke: {
            curve: "straight"
          },
          markers: {
            size: 0
         },
        series: [{
          name: 'sales',
          data: result
        },
        {
            name: 'target',
            data: target,
        }],
        xaxis: {
          type: 'datetime'
        },
        tooltip: {
            enabled:true,
            x: {
                show: true,
                format: 'HH:mm',
                formatter: undefined,
            },
        }
      }
      
      var chart = new ApexCharts(document.querySelector("#chart"), options);
      
      chart.render();
    });
   }
init();