let month = 1
let index = month * 2
//document.getElementById("demo").innerHTML = totalWeight
let width = 1200
let height = 600
let padding = 60

let svg = d3.select('svg')

let tickLabels = ["12AM", "1AM", "2AM","3AM","4AM","5AM","6AM","7AM","8AM","9AM","10AM","11AM","12PM","1PM","2PM","3PM","4PM","5PM","6PM","7PM","8PM","9PM","10PM","11PM"]

let xScale
let yScale

let minTime
let maxTime
let maxPercent

let ticksAmount = numberOfSteps
let tickStep = (ticksAmount - 0)/ ticksAmount
let step = Math.ceil((tickStep/5)*5)

let values = []


let canvas = d3.select('#canvas')
canvas.attr('width',width)
canvas.attr('height',height)

let generateScales = () => {


    xScale = d3.scaleLinear().domain([hoursStartTime,  hoursStartTime + numberOfSteps]).range([padding,width-padding])

    yScale = d3.scaleTime().domain([new Date(0,0,0,0,0,0,0), new Date(0,12,0,0,0,0,0)]).range([padding,height-padding])

}
let drawCells = ()=>{


  let dict = {}
  let countValue = 1
  let timeValue = 0
  let tempStartTime = hoursStartTime + 1
  let timeValueReset = false
  let resetCount = false

  for (let i = 0; i < numberOfSteps * 12; i++) {

    if(i < (numberOfSteps * countValue)){
      if(resetCount == true){
        tempStartTime = hoursStartTime + 1
        timeValue = 0
        resetCount = false
      }

      dict = {
        Month: countValue,
        time: data.Month[countValue - 1]["month_"+String(countValue - 1)].Time[timeValue][String(tempStartTime)].time,
        weight: data.Month[countValue - 1]["month_"+String(countValue - 1)].Time[timeValue][String(tempStartTime)].connectedValue
      }

      values.push(dict)
      tempStartTime = tempStartTime + 1
      timeValue = timeValue + 1

    }

    else{
      countValue = countValue + 1
      resetCount = true
      i = i - 1
    }
  }

  maxPercent = d3.max(values,(item)=>{
    return item.weight
  })/totalWeight


  canvas.selectAll('rect').data(values).enter().append('rect').attr('class','cell')
  .attr('fill', (item) => {
    let weight = item.weight
    if(weight == 0){
      return 'LightGray'
    }
    else if(weight < totalWeight * (0.0005)){
      return 'blue'
    }

    else if (weight < totalWeight * (0.001)){
      return 'powderblue'
    }
    else if(weight< totalWeight * (0.0015)){
      return 'aqua'
    }
    else if(weight< totalWeight * (0.002)){
      return 'aquamarine'
    }
    else if(weight< totalWeight * (0.0025)){
      return 'lightgreen'
    }
    else if(weight< totalWeight * (0.003)){
      return 'lime'
    }
    else if(weight< totalWeight * (0.0035)){
      return 'limegreen'
    }
    else if(weight< totalWeight * (0.0040)){
      return 'yellowgreen'
    }
    else if(weight< totalWeight * (0.0045)){
      return 'yellow'
    }
    else if(weight< totalWeight * (0.005)){
      return 'gold'
    }
    else if(weight< totalWeight * (0.0055)){
      return 'goldenrod'
    }
    else if(weight< totalWeight * (0.006)){
      return 'chocolate'
    }
    else if(weight< totalWeight * (0.0065)){
      return 'orange'
    }
    else if(weight< totalWeight * (0.007)){
      return 'darkorange'
    }
    else if(weight< totalWeight * (0.0075)){
      return 'orangered'
    }
    else if(weight< totalWeight * (0.008)){
      return 'tomato'
    }
    else if(weight< totalWeight * (0.0085)){
      return 'red'
    }
    else if(weight< totalWeight * (0.009)){
      return 'firebrick'
    }
    else if(weight< totalWeight * (0.0095)){
      return 'maroon'
    }
    else if(weight < totalWeight * (maxPercent)){
      return 'darkred'
    }
    else {
      return 'black'
    }



  })
  .attr('data-month', (item) =>{


      return item.Month


  })
  .attr('data-time', (item) =>{
    return item.time
  })
  .attr('data-weight', (item) => {
    return item.weight
  })
  .attr('height', (item) =>{
    return (height - (2*padding))/12
  })
  .attr('y', (item) =>{
    return yScale(new Date(0,item.Month - 1,0,0,0,0,0))
  })
  .attr('width',(item)=>{
    return (width - (2*padding))/numberOfSteps
  })
  .attr('x',(item) =>{
    return xScale(item.time - 1)
  })
}

let drawCanvas = () => {
    svg.attr('width', width)
    svg.attr('height', height)
}


let generateAxes = () => {

    let xAxis = d3.axisBottom(xScale).ticks(ticksAmount).tickFormat((d,i) => tickLabels[hoursStartTime + i]).tickSize(-(height - (2*padding)));
    let yAxis = d3.axisLeft(yScale).tickFormat(d3.timeFormat('%B')).tickSize(-(width - (2* padding)))
    for(let i = hoursStartTime; i < numberOfSteps + hoursStartTime + 1;i++){
    }

    canvas.append('g').call(xAxis).attr('id','Time').attr('transform','translate(0,'+(height-padding)+')')
    canvas.append('g').call(yAxis).attr('id','Months').attr('transform','translate('+padding+',0)')
}

drawCanvas()

generateScales()
drawCells()
generateAxes()
