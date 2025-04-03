import ShotsGeneratedByPlayerInPOIU from "../charts/ShotsGeneratedByPlayerInPOIU"
import SimilarityNetworkGraph from "../charts/SimilarityNetworkGraph"
import ShotsForScatterPlot from "../charts/ShotsForScatterPlot"


// this should have all of the charts and the
export default function POIUnitAnalysis({id}) {
  return <>
    <ShotsForScatterPlot id={id} />
    <SimilarityNetworkGraph id={id} />
    <ShotsGeneratedByPlayerInPOIU id={id} />

  </>
}