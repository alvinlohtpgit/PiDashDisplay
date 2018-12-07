
  tday=new Array("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday");
  tmonth=new Array("January","February","March","April","May","June","July","August","September","October","November","December");

  function GetClock(){
      var d=new Date();
      var nday=d.getDay(),nmonth=d.getMonth(),ndate=d.getDate(),nyear=d.getYear();
      if(nyear<1000) nyear+=1900;
      var nhour=d.getHours(),nmin=d.getMinutes(),nsec=d.getSeconds(),ap;

      if(nhour==0){ap=" AM";nhour=12;}
      else if(nhour<12){ap=" AM";}
      else if(nhour==12){ap=" PM";}
      else if(nhour>12){ap=" PM";nhour-=12;}

      if(nmin<=9) nmin="0"+nmin;
      if(nsec<=9) nsec="0"+nsec;

      document.getElementById('datedisplaypanel').innerHTML=""+tday[nday]+", "+tmonth[nmonth]+" "+ndate+", "+nyear+" "+nhour+":"+nmin+ap+"";
  }


  $(document).ready(function(){


      function loadWeatherAndTemp(){
          // On page load, get the weather
        $.ajax({
          method: "GET",
          url: "getWeather"
        }).done(function( msg ) {
            // Display the image
            if (msg.includes('Thundery Showers') == true){
                $("#weatherimagepanel").html("<img src='/static/PiDashDisplay/images/thundershower.png' />");
            }
            else if (msg == "Showers"){
                $("#weatherimagepanel").html("<img src='/static/PiDashDisplay/images/shower.png' />");
            }
            else if ((msg == "Light Showers") || (msg == "Light Rain")){
                $("#weatherimagepanel").html("<img src='/static/PiDashDisplay/images/lightshower.png' />");
            }
            else if (msg == "Partly Cloudy"){
                $("#weatherimagepanel").html("<img src='/static/PiDashDisplay/images/partlycloudy.png' />");
            }
            else if (msg == "Cloudy"){
                $("#weatherimagepanel").html("<img src='/static/PiDashDisplay/images/cloudy.png' />");
            }
            else if (msg == "Fair"){
                $("#weatherimagepanel").html("<img src='/static/PiDashDisplay/images/sunny.png' />");
            }

            // Update the span text to display the weather
            $("#forecastdisplaypanel").html(msg);
        });

        // On page load, get the temperature also
        $.ajax({
          method: "GET",
          url: "getTemp"
        }).done(function( msg ) {
            // Update the span text to display the weather
            $("#tempdisplaypanel").html(msg);
        });
      }

      GetClock();
      loadWeatherAndTemp();
      setInterval(GetClock,1000);
      setInterval(loadWeatherAndTemp, 1800000);

  }); // Close document ready

