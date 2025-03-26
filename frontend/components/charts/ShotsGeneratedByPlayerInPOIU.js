import * as d3 from "d3";

import { useEffect, useRef } from "react"

import {
  useQuery,
  useQueryClient
} from '@tanstack/react-query'

import { useGlobalState } from "../state_providers/GlobalState";

import { getShotsByPOIU } from "@/utils/api/players"
import { groupBy } from "@/utils/jsHelpers";

// the id is a poiu id.
export default function ShotsGeneratedByPlayerInPOIU({id}) {
  const queryClient = useQueryClient();
  const ref = useRef();
  const {maxYAxis, setMaxYAxisIfMax} = useGlobalState()

  // async state management
  const QUERY_KEY_SHOTS_BY_POIU = `getShotsByPOIU-${id}`
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

  // everything below here is d3.js or used by d3.js
  const MAX_WIDTH = 620
  const MAX_HEIGHT = 420
  const margin = { top: 50, right: 20, bottom: 50, left: 50 },
    width = MAX_WIDTH - margin.left - margin.right,
    height = MAX_HEIGHT - margin.top - margin.bottom

  // listen to the change in the data and
  // renders the barchart if the data has changed
  useEffect(()=> {
    if (!data) return
    createOrUpdateBarChart()
  }, [id, data, maxYAxis])

  const createOrUpdateBarChart = () => {
    // groups players together.
    let shotsForByPlayersData = groupBy(data.shots_for, "shooterName")
    console.log(shotsForByPlayersData)

    // format the data so that it can be used in groups
    let formattedDataForChart = []
    Object.keys(shotsForByPlayersData).map((player)=> {
      // console.log("LOOOK HERE")
      let playerShotData = shotsForByPlayersData[player]
      // formattedDataForChart = {}
      let formattedPlayerData = {
        key: player,
        value: {}
      }

      formattedPlayerData.value["shots"] = playerShotData.length
      // get the goals
      formattedPlayerData.value["goals"] = playerShotData.reduce((result, shotData)=> {
        return result + shotData.goal
      }, 0)
      // get the missed shots by events
      formattedPlayerData.value["missed"] =playerShotData.reduce((result, shotData)=> {
        console.log(shotData.event)
        if (shotData.event == "MISS") {
          return result + 1
        }
        return result
      }, 0)
      formattedPlayerData.value["player"] = player
      formattedDataForChart.push(formattedPlayerData)
    })

    // delete everything in the svg
    d3.select(ref.current).selectAll("*").remove();
    // append the svg object to the body of the page
    const svg = d3
      .select(ref.current)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // group the players by their names.
    const groups = Object.keys(shotsForByPlayersData)
    const subGroups = ["goals", "missed", "shots"  ]

    // get max shots
    const shotsByPlayers = formattedDataForChart.map((shotDataByPlayer)=> {
      return shotDataByPlayer.value.shots
    })
    // setMaxYAxisIfMax for all of the charts so that they're consistent.
    setMaxYAxisIfMax(Math.max(...shotsByPlayers))

    // create scales
    const xScaleOuter = d3.scaleBand()
      .domain(groups)
      .range([0, width])
      .padding(0.2)

    const xScaleInner = d3.scaleBand()
      .domain(subGroups)
      .range([0, xScaleOuter.bandwidth()])
      .padding(0.05);

    const yScale = d3.scaleLinear()
      .domain([0, maxYAxis])
      .range([height, 0]);

    // add axes
    svg.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(xScaleOuter))
      .selectAll("text")
      .style("font-size", "12px");

    svg.append("g")
      .call(d3.axisLeft(yScale));

    // add labels
    // Axis Labels
    svg.append("text")
      .attr("x", width / 2)
      .attr("y", height + margin.top - 10)
      .attr("text-anchor", "middle")
      .attr("class", "axis-label")
      .text("Players");

    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("x", -height / 2)
      .attr("y", -margin.left/2)
      .attr("text-anchor", "middle")
      .attr("class", "axis-label")
      .text("Count of Goals/Shots/Missed");

    // title
    svg.append("text")
    .attr("id", "title")
      .attr("x", margin.right +40)
      .attr("y", -margin.top/2)
      .attr("class", "title")
      .text("Shots, Goals and Missed shots when playing as a unit")

    // colors
    // note colors from https://colorbrewer2.org/#type=diverging&scheme=Spectral&n=3
    const color = d3.scaleOrdinal()
      .domain(subGroups)
      .range([
        "#99d594",
        "#fc8d59",
        "#ffffbf",
      ]);

    svg.selectAll("g.bar-group")
      .data(formattedDataForChart)
      .enter()
      .append("g")
      .attr("class", "bar-group")
      .attr("transform", d => `translate(${xScaleOuter(d.key)}, 0)`)
      .selectAll("rect")
      .data((d)=> {
        let grouping = subGroups.map((group)=> {
          return {
            key: group,
            value: d.value[group]
          }
        })
        return grouping
      })
      .enter()
      .append("rect")
      .attr("x", d => {
        let x = xScaleInner(d.key)

        return x
      })
      .attr("y", d => {
        let y = yScale(d.value)
        return y
      })
      .attr("width", xScaleInner.bandwidth())
      .attr("height", d => height - yScale(d.value))
      .attr("fill", d => color(d.key))
      .attr("class", "bar");

    // create legend
    const legend = svg.append("g")
        .attr("transform", `translate(${width - margin.right - margin.left}, ${0})`);

    subGroups.forEach((group, i) => {
        const legendRow = legend.append("g")
            .attr("transform", `translate(0, ${i * 20})`);

        legendRow.append("rect")
            .attr("width", 15)
            .attr("height", 15)
            .attr("fill", color(group));

        legendRow.append("text")
            .attr("x", 20)
            .attr("y", 12)
            .attr("text-anchor", "start")
            .style("font-size", "12px")
            .text(group);
    });
  }

  // guard if there's no data.
  if (isLoading) {
    return <div width={MAX_WIDTH} height={MAX_HEIGHT}>
      Loading Shot Generated by player chart...
    </div>
  }
  if (!data) {
    return <div width={MAX_WIDTH} height={MAX_HEIGHT}></div>
  }

  return <div width={MAX_WIDTH} height={MAX_HEIGHT}>
    <svg width={MAX_WIDTH} height={MAX_HEIGHT} id={`shots-for-by-${id}`} ref={ref} />
  </div>
}