/* globals Chart:false */
const lanes = [
    { id: 1, vehicles: 0, light: "red" },
    { id: 2, vehicles: 0, light: "red" },
    { id: 3, vehicles: 0, light: "red" },
    { id: 4, vehicles: 0, light: "red" },
  ]
  
  // Function to render the traffic simulation
  function renderTrafficSimulation() {
    const trafficSimulation = document.getElementById("traffic-simulation")
    trafficSimulation.innerHTML = ""
  
    lanes.forEach((lane) => {
      const laneElement = document.createElement("div")
      laneElement.className = "lane"
      laneElement.innerHTML = `
              <h2>Lane ${lane.id}</h2>
              <div class="traffic-light">
                  <div class="light ${lane.light === "red" ? "red" : "off"}"></div>
                  <div class="light ${lane.light === "yellow" ? "yellow" : "off"}"></div>
                  <div class="light ${lane.light === "green" ? "green" : "off"}"></div>
              </div>
              <div class="vehicle-counter">
                  <span>Vehicles: ${lane.vehicles}</span>
                  <div>
                      <button onclick="changeVehicleCount(${lane.id}, -1)">-</button>
                      <button onclick="changeVehicleCount(${lane.id}, 1)">+</button>
                  </div>
              </div>
          `
      trafficSimulation.appendChild(laneElement)
    })
  }
  
  // Function to change vehicle count
  function changeVehicleCount(laneId, change) {
    const lane = lanes.find((l) => l.id === laneId)
    lane.vehicles = Math.max(0, lane.vehicles + change)
    renderTrafficSimulation()
  }
  
  // Function to update traffic lights
  function updateTrafficLights() {
    const maxVehiclesLane = lanes.reduce((max, lane) => (lane.vehicles > max.vehicles ? lane : max))
  
    lanes.forEach((lane) => {
      lane.light = lane.id === maxVehiclesLane.id ? "green" : "red"
    })
  
    renderTrafficSimulation()
  }
  
  // Initial render
  renderTrafficSimulation()
  
  // Update traffic lights every 5 seconds
  setInterval(updateTrafficLights, 5000)



  
(() => {
    'use strict'
  
    // Graphs
    const ctx = document.getElementById('myChart')
    // eslint-disable-next-line no-unused-vars
    const myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [
          'Sunday',
          'Monday',
          'Tuesday',
          'Wednesday',
          'Thursday',
          'Friday',
          'Saturday'
        ],
        datasets: [{
          data: [
            15339,
            21345,
            18483,
            24003,
            23489,
            24092,
            12034
          ],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          borderWidth: 4,
          pointBackgroundColor: '#007bff'
        }]
      },
      options: {
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            boxPadding: 3
          }
        }
      }
    })


    // Initialize lanes

  
  
  })()
  