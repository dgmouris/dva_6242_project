import { useEffect } from 'react'

import {
  useQuery,
  useQueryClient
} from '@tanstack/react-query'

import POIUnitCard from "@/components/poiu/POIUnitCard"

import { useGlobalState } from '../state_providers/GlobalState'

import { getSimilarUnitsByPoiu } from '@/utils/api/players'

export default function SimilarPOIUSection() {
  const queryClient = useQueryClient();
  const {
    currentPlayer,
    currentPlayerPOIU,
    currentSimilarPOIU,
    currentSituation,
    allPlayerMatchPOIUs,
    setCurrentSimilarPOIU,
    setAllSimilarPOIUs
  } = useGlobalState()

  const getSimilarPOIUs = async () => {
    if (!currentPlayerPOIU) return
    const data = await getSimilarUnitsByPoiu({
      poiuId: currentPlayerPOIU,
      situation: currentSituation
    })
    console.log("getSimilarPOIUs")
    console.log(data)

    // set the list used for the select
    setAllSimilarPOIUs(data)
    // get the first item and pass it in
    // this will be changed from the select
    setCurrentSimilarPOIU(data[0])
    return data
  }

  let { isPending, error, data, refetch } = useQuery({
    queryKey: [`getSimilarUnitsByPoiu`],
    queryFn: async ()=> {
      return await getSimilarPOIUs()
    },
    enabled: false, // this will only fetch once you get a player
    staleTime: Infinity,
  })

  // listen to changes in the current poiu and fetch it.
  useEffect(()=> {
    if (!currentPlayer) return // guard
    if (!currentPlayerPOIU) return // guard
    console.log("FETCHED HERE")
    queryClient.invalidateQueries(`getSimilarUnitsByPoiu`)
    refetch()

  }, [currentPlayer, currentSituation, currentPlayerPOIU, setCurrentSimilarPOIU])

  // if no player show nothing.
  if (!currentPlayer) {
    return <></>
  }


  if (isPending) {
    return "Loading..."
  }

  return <>
    <POIUnitCard
      team={currentPlayer.fullTeamName.default}
      isSimilarMatchPOIU={true}
      isPlayerMatchPOIU={false}
      unitId={currentSimilarPOIU}
    />
  </>

}