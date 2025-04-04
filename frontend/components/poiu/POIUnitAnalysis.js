import ShotsGeneratedByPlayerInPOIU from "../charts/ShotsGeneratedByPlayerInPOIU"
import SimilarityNetworkGraph from "../charts/SimilarityNetworkGraph"
import ShotsForScatterPlot from "../charts/ShotsForScatterPlot"
import ShotsAgainstHeatMapPlot from "../charts/ShotsAgainstHeatMapPlot"

// this should have all of the charts and the
export default function POIUnitAnalysis({id}) {
  return <>
    <SimilarityNetworkGraph id={id} />
    <ShotsForScatterPlot id={id} />
    <ShotsAgainstHeatMapPlot id={id} />
    <ShotsGeneratedByPlayerInPOIU id={id} />

  </>
}