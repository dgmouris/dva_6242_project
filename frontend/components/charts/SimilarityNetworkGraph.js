import '@/styles/similarity_network_graph.css'

import * as d3 from "d3"

import { useEffect, useRef } from "react"

import {
  useQuery,
  useQueryClient
} from '@tanstack/react-query'

import { useGlobalState } from "../state_providers/GlobalState"

import { getSimilarityPoiuStatsByPoiu } from "@/utils/api/players"

export default function SimilarityNetworkGraph({id}) {
  const queryClient = useQueryClient()
  const ref = useRef()

  const {
    currentPlayerPOIU,
    currentSimilarPOIU
  } = useGlobalState()


  // async state management
  const SIMILAR_POIUS = `getSimilarityPoiuStatsByPoiu-${id}`
  let { isLoading, error, data, refetch } = useQuery({
    queryKey: [SIMILAR_POIUS],
    queryFn: async ()=> {
      return await getSimilarityPoiuStatsByPoiu({poiu: id})
    },
    enabled: false, // this will only fetch once you get a player
    staleTime: Infinity,
  })
  // listen to changes in the id and refetch a different poiu
  useEffect(()=> {
    if (!id) return // guard

    if (!data) {
      queryClient.invalidateQueries(SIMILAR_POIUS)
      refetch()
    }
  }, [id])

  // everything below here is d3.js or used by d3.js
  const MAX_WIDTH = 620
  const MAX_HEIGHT = 720
  const margin = { top: 100, right: 20, bottom: 50, left: 50 },
    width = MAX_WIDTH - margin.left - margin.right,
    height = MAX_HEIGHT - margin.top - margin.bottom

  // listen to the change in the data and
  // renders the barchart if the data has changed
  useEffect(()=> {
    if (!data) return
    createOrUpdateBarChart()
  }, [
    id, data,
    // needs to update on poius being set.
    currentPlayerPOIU, currentSimilarPOIU
  ])

  const createOrUpdateBarChart = () => {
    // the nodes of the graph is the data
    // including the base poiu
    const nodes = [data.base_poiu, ...data.similar_poius]
    // for the network all of the data is going to have the
    // same target which is the base_poiu
    const links = data.similar_poius.map((similarPoiu, index)=> {
      let link = {
        source: similarPoiu.id,
        target: data.base_poiu.id,
        rank: index + 1, // this is so that we can see the rank of the connection
        percentage: similarPoiu.similarity,
        ...similarPoiu
      }
      return link
    })

    // delete everything in the svg
    d3.select(ref.current).selectAll("*").remove()

    let simulation;

    // create the draggability and check if the simulation exists
    // these are defined in here because they need access
    // to the simulation
    const dragStarted = (event, d) => {
      if (!simulation) {return}
      if (!event.active) {
        simulation.alphaTarget(0.3).restart()
      }
      d.fx = d.x
      d.fy = d.y
    }

    const dragged = (event, d) => {
        if (!simulation) {return}
        d.fx = event.x
        d.fy = event.y
    }

    const dragEnded = (event, d) => {
        if (!simulation) {return}
        if (!event.active) {
          simulation.alphaTarget(0)
        }
        d.fx = null
        d.fy = null
    }

    // create the graph for similarity
    const svg = d3
      .select(ref.current)

    const colors = [
      "green",
      "orange",
      "lightblue"
    ]
    const MATCHED_POIU_INDEX = 0
    const SIMILAR_POIU_SELECTED_INDEX = 1
    const SIMILAR_POIU_INDEX = 2

    const colorLabels = [
      "Matched POIU",
      "Selected Similar POIU",
      "Similar POIU"
    ]


    simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(d => {
        // similar ones closer
        let closer = (100-d.percentage)
        // think about a cool way to do this.
        return 240
      }))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter((width+margin.left) / 2, (height+margin.top) / 2))

    const link = svg.append("g")
      .selectAll("line")
      .data(links)
      .enter().append("line")
      .attr("class", "link")

    const linkLabels = svg.append("g")
      .selectAll("text")
      .data(links)
      .enter().append("text")
      .attr("class", "label")
      .attr("text-anchor", "middle")
      .text(d => d.percentage)

    const node = svg.append("g")
      .selectAll("g")
      .data(nodes)
      .enter().append("g")
      .attr("class", "node")
      .call(d3.drag()
          .on("start", dragStarted)
          .on("drag", dragged)
          .on("end", dragEnded))

    // Main node circle
    node.append("circle")
      .attr("r", 98)
      .attr("fill", (d) => {
        if (d.id === currentPlayerPOIU) {
          return "green"
        }
        if (d.id === currentSimilarPOIU) {
          return "orange"
        }

        return "lightblue"
      })
      .attr("stroke", "black")
      .attr("stroke-width", 2)

    // lots of tweaking here.
    const scale = 2.05
    // Positions for inner circles (arranged in a pentagon shape)
    const innerOffsets = [
      { x: 18*scale, y: -24*scale },
      { x: -18*scale, y: -24*scale },
      { x: 28*scale, y: 10*scale },
      { x: -28*scale, y: 10*scale },
      { x: 0*scale, y: 32*scale }
    ]

    // append all inner circles
    node.selectAll(".inner-circle")
      .data(d => innerOffsets.map((offset, i) => ({ parent: d, index: i + 1, x: offset.x, y: offset.y })))
      .enter()
      .append("circle")
      .attr("class", "inner-circle")
      .attr("r",35)
      .attr("fill", "black")
      .attr("cx", d => d.x)
      .attr("cy", d => d.y)

    // append inner labels
    node.selectAll(".inner-label")
      .data(d => {
        return innerOffsets.map((offset, i) => ({ parent: d, index: i + 1, x: offset.x, y: offset.y }))
      })
      .enter()
      .append("text")
      .attr("class", "inner-label")
      .attr("x", d => d.x)
      .attr("y", d => d.y + 3) // Adjust for vertical alignment
      .text(d => {
        let player = d.parent.players[d.index - 1]
        // the index is going to be the offset that we're going to fetch from the
        // players
        let fullName = d.index
        // until we have the player information
        let firstSpace = player.full_name.indexOf(' ')
        fullName = player.full_name.slice(firstSpace + 1) // from the data base
        // try to get the last name
        return fullName

      });

    // create the similarity
    simulation.on("tick", () => {
      link.attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

      linkLabels.attr("x", d => (d.source.x + d.target.x) / 2)
                .attr("y", d => (d.source.y + d.target.y) / 2 - 5);

      node.attr("transform", d => `translate(${d.x},${d.y})`);
    });

    // title
    svg.append("text")
      .attr("id", "title")
      .attr("x", margin.right)
      .attr("y", margin.top/2)
      .attr("class", "title")
      .text("Similar POIU percentages")

  }



  // guard if there's no data.
  if (isLoading) {
    return <div width={MAX_WIDTH} height={MAX_HEIGHT}>
      Loading Similar POIU chart...
    </div>
  }

  if (!data) {
    return <div width={MAX_WIDTH} height={MAX_HEIGHT}></div>
  }



  return <div width={MAX_WIDTH} height={MAX_HEIGHT}>
    <svg width={MAX_WIDTH} height={MAX_HEIGHT} id={`similar-poius-${id}`} ref={ref} />
  </div>

}