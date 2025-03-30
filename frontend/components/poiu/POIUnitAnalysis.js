import ShotsGeneratedByPlayerInPOIU from "../charts/ShotsGeneratedByPlayerInPOIU"
import SimilarityNetworkGraph from "../charts/SimilarityNetworkGraph"

// this should have all of the charts and the
export default function POIUnitAnalysis({id}) {
  return <>
    <SimilarityNetworkGraph id={id} />
    <ShotsGeneratedByPlayerInPOIU id={id} />

  </>
}