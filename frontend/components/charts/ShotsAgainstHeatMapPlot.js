import '@/styles/shot_scatter_plot.css'

import * as d3 from "d3";

import { useEffect, useRef } from "react"

import {
  useQuery,
  useQueryClient
} from '@tanstack/react-query'

import { groupBy } from "@/utils/jsHelpers";

import { getShotsByPOIU } from "@/utils/api/players"

export default function ShotsAgainstHeatMapPlot({id}) {
  const queryClient = useQueryClient();
  const ref = useRef()

  // async state management
  const QUERY_KEY_SHOTS_BY_POIU = `getShotsForScatterByPOIU-${id}`
  let { isLoading, error, data, refetch } = useQuery({
    queryKey: [QUERY_KEY_SHOTS_BY_POIU],
    queryFn: async ()=> {
      return await getShotsByPOIU({poiu: id})
    },
    enabled: false, // this will only fetch once you get a player
    staleTime: Infinity,
  })

  // listen to changes in the id and refetch a different poiu
  useEffect(()=> {
    if (!id) return // guard

    queryClient.invalidateQueries(QUERY_KEY_SHOTS_BY_POIU)
    if (!data) {
      refetch()
    }
  }, [id])

  useEffect(()=> {
    if (!data) {
      return
    }

    createHeatMapChart()

  }, [data])

  const MAX_WIDTH = 550
  const MAX_HEIGHT = 533
  const margin = { top: 70, right: 20, bottom: 50, left: 50 },
    width = MAX_WIDTH - margin.left - margin.right,
    height = MAX_HEIGHT - margin.top - margin.bottom

  const createHeatMapBins = (xDimensions, yDimensions, binSize) => {
    const top = yDimensions[1]
    const bottom = yDimensions[0]
    const left = xDimensions[0]
    const right = xDimensions[1]

    let rows = Array((left+right)/binSize).fill(0)
    let columns = Array((Math.abs(top) + Math.abs(bottom))/binSize).fill([])
    let allBins = columns.map((col)=> {
      let row = Array((left+right)/binSize).fill(0)
      console.log(row)
      return row
    })
    return allBins
  }

  const assignShotToHeatMapBins = (shotsAgainst, heatMapBins, binSize) => {
    shotsAgainst.map((shot)=> {
      const RINK_Y_OFFSET = 42.5 // this is going to make it so that you can access the bin size
      let xBin = Math.floor(shot.xCordAdjusted/binSize)
      let yBin = Math.floor(((shot.yCordAdjusted+RINK_Y_OFFSET)/binSize))

      // add one to the bins
      heatMapBins[yBin][xBin] += 1

    })
    return heatMapBins
  }


  const createHeatMapChart = () => {

    // x domain
    let yDomain = [-42.5, 42.5] // the dimensions of a hockey rink
    let xDomain = [0, 100] // half the length of a hockey rink


    // size of the defensive bins
    let binSize = 5 // translate to feet for binSize

    let heatMapBins = createHeatMapBins(xDomain, yDomain, binSize)
    // console.log("heatMapBins")
    // console.log(heatMapBins)
    // create an array for the test data for all the heat map bins


    // colors from https://colorbrewer2.org/#type=qualitative&scheme=Paired&n=5

    // group by games so that you can get the average.
    let shotsByGameAgainst = groupBy(data.shots_against, "game_id")
    let gamesPlayerTogether = Object.keys(shotsByGameAgainst).length

    // remove and add.
    d3.select(ref.current).selectAll("*").remove();


    const shotHeatMapBins = assignShotToHeatMapBins(data.shots_against, heatMapBins, binSize)

    const maxShotsAgainstPerGame = Math.max(...shotHeatMapBins.flat())

    const colorScale = d3.scaleSequential(d3.interpolateInferno)
    .domain([0, maxShotsAgainstPerGame]);

    // when createing the svg
    const svg = d3
    .select(ref.current)
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
      "translate(" + margin.left + "," + margin.top + ")");




    let testData = heatMapBins

    // get the height
    const numRows = testData.length;
    const numCols = testData[0].length;
    const cellWidth = width/numCols;
    const cellHeight = height/numRows;


    svg.append('image')
      .attr('href', 'NHL_Hockey_Rink_half_formatted.png')
      .attr('width', width)
      .attr('height', height)
      .attr("class", "arena-image")


    svg.selectAll("g")
    .data(testData)
    .join("g")
    .attr("transform", (d, i) => `translate(0, ${i * cellHeight})`)
    .selectAll("rect")
    .data(d => d)
    .join("rect")
    .attr("class", "cell")
    .attr("x", (d, i) => i * cellWidth)
    .attr("width", cellWidth)
    .attr("height", cellHeight)
    .attr("fill", d => {
      const COLOR_AMPLIFIER = 5 // just to make this brighter
      let shotsPerGame = d/gamesPlayerTogether*COLOR_AMPLIFIER

      const color = `rgba(255, 0, 0, ${shotsPerGame})`
      return color;
    });



    // // add title
    svg.append("text")
    .attr("id", "title")
      .attr("x", margin.right +40)
      .attr("y", -margin.top+40)
      .attr("class", "title")
      .text(`Shots Against when playing together (bins size of ${binSize} ft)`)

      // Add X axis
    let xScale = d3.scaleLinear()
      .domain(xDomain)
      .range([ 0, width ]);

      svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(xScale));

    // Add Y axis
    let yScale = d3.scaleLinear()
      .domain(yDomain)
      .range([ height, 0]);
    svg.append("g")
      .call(d3.axisLeft(yScale));

  }

  if (isLoading) {
    return <div width={MAX_WIDTH} height={MAX_HEIGHT}>
      Loading Shot Scatter plot...
    </div>
  }
  if (!data) {
    return <div width={MAX_WIDTH} height={MAX_HEIGHT}></div>
  }

  return <div className="flex items-center justify-center ">
    <svg width={MAX_WIDTH} height={MAX_HEIGHT} id={`shots-for-by-${id}`} ref={ref} >

    </svg>
  </div>
}
