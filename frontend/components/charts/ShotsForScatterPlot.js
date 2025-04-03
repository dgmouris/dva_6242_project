import * as d3 from "d3";

import { useEffect, useRef } from "react"

import {
  useQuery,
  useQueryClient
} from '@tanstack/react-query'

export default function ShotsForScatterPlot({id}) {
  const queryClient = useQueryClient();
  const ref = useRef()

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

  useEffect(()=> {
    if (!data) {
      return
    }

    createScatterPlot()

  }, [data])

  const MAX_WIDTH = 620
  const MAX_HEIGHT = 420
  const margin = { top: 50, right: 20, bottom: 50, left: 50 },
    width = MAX_WIDTH - margin.left - margin.right,
    height = MAX_HEIGHT - margin.top - margin.bottom

  const createScatterPlot = () => {
    console.log("createScatterPlot")
    const shotsFor = data.shots_for

    // remove and add.
    d3.select(ref.current).selectAll("*").remove();

    // when createing the svg
    const svg = d3
      .select(ref.current)
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    // x domain
    let yDomain = [-42.5, 42.5] // the dimensions of a hockey rink
    let xDomain = [0, 100]


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

    // Add dots
    svg.append('g')
      .selectAll("dot")
      .data(shotsFor)
      .enter()
      .append("circle")
        .attr("cx", function (d) {

          console.log("cx")
          console.log(d)
          return xScale(d.xCordAdjusted)
        } )
        .attr("cy", function (d) {
          return yScale(d.yCordAdjusted)
        } )
        .attr("r", 4)
        .style("fill", "#69b3a2")
  }



  if (isLoading) {
    return <div width={MAX_WIDTH} height={MAX_HEIGHT}>
      Loading Shot Scatter plot...
    </div>
  }
  if (!data) {
    return <div width={MAX_WIDTH} height={MAX_HEIGHT}></div>
  }

  return <div width={MAX_WIDTH} height={MAX_HEIGHT}>
    <svg width={MAX_WIDTH} height={MAX_HEIGHT} id={`shots-for-by-${id}`} ref={ref} />
  </div>
}
