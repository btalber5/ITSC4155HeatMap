$("form[name=signup_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=login_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

window.onload = function () {
  document.getElementById('input-file').addEventListener('change', getFile)
  $("#tabs").tabs();
  $(".spinner").spinner();
  loadMap();
  loadTable();


  $(function () {
    $('*[name=date]').appendDtpicker();
  });
  google.charts.setOnLoadCallback(drawChart);
}

//Update Data
function updateData() {
  getAllPops();
  loadMap();
  loadTable();
  drawChart();
  $("#atkinsTime").html(timestamps[timestamps.length - 1]);
  timeStampFormat();

}


//load log file
//load file
function getFile(event) {
  const input = event.target
  if ('files' in input && input.files.length > 0) {
    placeFileContent(
      document.getElementById('content-target'),
      input.files[0])
  }
}

//make arrays for the buildings
var contentWithOnlyWood = [];
var atkins = [];
var studentUnionPop = [];
var colv = [];
var cone = [];
var prospector = [];

//display log file
var contentNewLineSplitArray = [];
var contentWithOnlyAssoc = []
var timestamps = [];

function placeFileContent(target, file) {
  readFileContent(file).then(content => {
    target.value = content
    $(".filterBtn").click(

      //parse log files
      function parseLog() {

        //array for the buildings to be parsed
        contentWithOnlyWood = [];
        atkins = [];
        studentUnionPop = [];
        colv = []
        cone = []
        prospector = [];

        contentNewLineSplitArray = content.split('\n');

        contentWithOnlyAssoc = []
        //var substring;
        var substring = this.id;
        //var substring = "Deauth";

        for (var i = 0; i < contentNewLineSplitArray.length; i++) {
          if (contentNewLineSplitArray[i].includes(substring)) {
            contentWithOnlyAssoc.push(contentNewLineSplitArray[i])
            timestamps[i] = contentNewLineSplitArray[i].slice(0, 15);
            console.log(timestamps[i]);
          }
        }

        //woodward sort
        for (var i = 0; i < contentWithOnlyAssoc.length; i++) {

          if (contentWithOnlyAssoc[i].includes("Wood")) {
            contentWithOnlyWood.push(contentNewLineSplitArray[i])
          }
        }
        //atkins sort
        for (var i = 0; i < contentWithOnlyAssoc.length; i++) {

          if (contentWithOnlyAssoc[i].includes("Atki")) {
            atkins.push(contentNewLineSplitArray[i])
          }
        } //colvard sort
        for (var i = 0; i < contentWithOnlyAssoc.length; i++) {

          if (contentWithOnlyAssoc[i].includes("Colv")) {
            colv.push(contentNewLineSplitArray[i])
          }
        }
        //cone sort
        for (var i = 0; i < contentWithOnlyAssoc.length; i++) {

          if (contentWithOnlyAssoc[i].includes("StuU")) {
            studentUnionPop.push(contentNewLineSplitArray[i])
          }
        }
        //cone sort
        for (var i = 0; i < contentWithOnlyAssoc.length; i++) {

          if (contentWithOnlyAssoc[i].includes("Cone")) {
            cone.push(contentNewLineSplitArray[i])
          }
        } //prospector sort

        for (var i = 0; i < contentWithOnlyAssoc.length; i++) {

          if (contentWithOnlyAssoc[i].includes("Pros")) {
            prospector.push(contentNewLineSplitArray[i])
          }
        }

        target.value = contentWithOnlyAssoc.join("\r\n")

        //VERY IMPORTANT
        //how to get ARRAY to print each element on new line
        //target.value = printedArray.join("\r\n\n")
      })
  }).catch(error => console.log(error))
  updateData();
}


//format timestamps
function getMonth(string) {
  var month = string.slice(0, 3);
  console.log(month);

  return month;

}

function timeStampFormat() {
  for (var i = 0; i < timestamps.length; i++)
    var month = getMonth(timestamps[i]);
  //console.log(month);
}


//get populations
function calcPop(location) {
  var population = 0;
  for (var i = 0; i < contentWithOnlyAssoc.length; i++) {
    if (contentWithOnlyAssoc[i].includes(location)) {
      population++;
    }
  }
  return population;
}


//count Population
//count Population
var atkinsPop = 0;
var woodwardPop = 0;
var unionPop = 0;
var epicPop = 0;
var coedPop = 0;
var fretwelPop = 0;
var colvardPop = 0;
var conePop = 0;
var dukePop = 0;
var robinsonPop = 0;
var rowePop = 0;
var belkPop = 0;
var gagePop = 0;
var huntPop = 0;
prospectorPop = 0;

function getAllPops() {
  atkinsPop = calcPop("Atki");
  woodwardPop = calcPop("Wood");
  unionPop = calcPop("StuU");
  epicPop = calcPop("keyword");
  fretwellPop = calcPop("keyword");
  colvardPop = calcPop("Colv");
  conePop = calcPop("Cone");
  rowePop = calcPop("Rowe");
  belkPop = calcPop("keyword");
  gagePop = calcPop("Gage");
  huntPop = calcPop("keyword");
  prospectorPop = calcPop("Pros");
  robinsonPop = calcPop("Robi");
  //TODO: add all other locations
}

function readFileContent(file) {
  const reader = new FileReader()
  return new Promise((resolve, reject) => {
    reader.onload = event => resolve(event.target.result)
    reader.onerror = error => reject(error)
    reader.readAsText(file)
  })
}




function loadMap() {
  var uncc = new google.maps.LatLng(35.307564, -80.735759);

  var woodward = new google.maps.LatLng(35.307345, -80.735652);
  var union = new google.maps.LatLng(35.308906, -80.733758);
  var atkins = new google.maps.LatLng(35.305850, -80.732149);
  var atkins1 = new google.maps.LatLng(35.305653, -80.731657);
  var atkins2 = new google.maps.LatLng(35.305964, -80.732521);
  var epic = new google.maps.LatLng(35.309097, -80.741713);
  var fretwell = new google.maps.LatLng(35.306057, -80.729141);
  var colvard = new google.maps.LatLng(35.304845, -80.731715);
  var cone = new google.maps.LatLng(35.305122, -80.733254);
  var duke = new google.maps.LatLng(35.312063, -80.741291);
  var robinson = new google.maps.LatLng(35.303894, -80.729934);
  var rowe = new google.maps.LatLng(35.304644, -80.730759);
  var belk = new google.maps.LatLng(35.306394, -80.729969);
  var gage = new google.maps.LatLng(35.300717, -80.734088);
  var hunt = new google.maps.LatLng(35.301420, -80.736445);

  var heatMapData = [{
      location: woodward,
      weight: woodwardPop
    },
    {
      location: union,
      weight: unionPop
    },
    {
      location: atkins,
      weight: atkinsPop / 3
    },
    {
      location: atkins1,
      weight: atkinsPop / 3
    },
    {
      location: atkins2,
      weight: atkinsPop / 3
    },
    {
      location: epic,
      weight: epicPop
    },
    {
      location: fretwell,
      weight: fretwelPop
    },
    {
      location: colvard,
      weight: colvardPop
    },
    {
      location: cone,
      weight: conePop
    },
    {
      location: duke,
      weight: dukePop
    },
    {
      location: robinson,
      weight: robinsonPop
    },
    {
      location: rowe,
      weight: rowePop
    },
    {
      location: belk,
      weight: belkPop
    },
    {
      location: gage,
      weight: gagePop
    },
    {
      location: hunt,
      weight: huntPop
    },
  ]

  var map = new google.maps.Map(document.getElementById('map'), {
    center: uncc,
    zoom: 16,
    dissipating: false,
    maxIntensity: 500
  });

  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatMapData,
    radius: 10
  });
  heatmap.setMap(map);
}

//GRAPHS

// Load the Visualization API and the corechart package.
google.charts.load('current', {
  'packages': ['corechart']
});

// Set a callback to run when the Google Visualization API is loaded.


// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.



function drawChart() {
  // Create the data table.
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Topping');
  data.addColumn('number', 'Slices');

  //Get the length of the array
  data.addRows([
    ['Student Union', unionPop],
    ['Woodward', woodwardPop],
    ['Atkins', atkinsPop],
    ['Cone', conePop],
    ['Colvard', colvardPop],
    ['Prospector', prospectorPop],
    ['Rowe', rowePop]
  ]);

  // Set chart options
  var options = {
    'title': 'Current Population on Campus',
    'width': 400,
    'height': 300,
    'pieHole': 0.4
  };

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.PieChart(document.getElementById('chart'));
  chart.draw(data, options);
}


//load table Data
function loadTable() {
  $("#atkinsTd").text(atkinsPop);
  $("#coedTd").text(coedPop);
  $("#coneTd").text(conePop);
  $("#colvardTd").text(colvardPop);
  $("#dukeTd").text(dukePop);
  $("#epicTd").text(epicPop);
  $("#fretwellTd").text(fretwelPop);
  $("#gageTd").text(gagePop);
  $("#huntTd").text(huntPop);
  $("#robinsonTd").text(robinsonPop);
  $("#roweTd").text(rowePop);
  $("#unionTd").text(unionPop);
  $("#woodwardTd").text(woodwardPop);
}