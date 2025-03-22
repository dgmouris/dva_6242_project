import { useEffect } from 'react'

import {
  useQuery,
  useQueryClient
} from '@tanstack/react-query'

import POIUnitCard from "@/components/poiu/POIUnitCard"

import { useGlobalState } from '../state_providers/GlobalState'

import { getUnitsByPlayerId } from "@/utils/api/players"

export default function PlayerMatchPOIUSection() {
  const queryClient = useQueryClient();
  const {
    currentPlayer,
    currentSituation,
    setCurrentPlayerPOIU,
    currentPlayerPOIU,
    setAllPlayerMatchPOIUs,
  } = useGlobalState()

  const getMatchedPOIUs = async () => {
    if (!currentPlayer) return // guard if there is no player.

    // call the backend.
    const data = await getUnitsByPlayerId({
      playerId: currentPlayer.playerId,
      situation:currentSituation
    })

    // set the list used for the select
    setAllPlayerMatchPOIUs(data)
    // get the first item and pass it in
    // this will be changed from the select
    setCurrentPlayerPOIU(data[0])

    // return the data incase we want to use it later.
    return data
  }

  let { isPending, error, data, refetch } = useQuery({
    queryKey: [`getUnitsByPlayerId`],
    queryFn: async ()=> {
      return await getMatchedPOIUs()
    },
    enabled: false, // this will only fetch once you get a player
    staleTime: Infinity,
  })


  // listen to the changes in player and situation and get and set the currentPOIU and allPlayerMatchPOIUs

  useEffect(()=> {
    if (!currentPlayer) return //

    queryClient.invalidateQueries(`getUnitsByPlayerId`)
    refetch()
  },[currentPlayer, currentSituation])


  // if no player show nothing.
  if (!currentPlayer) {
    return <></>
  }

  // console.log(isPending, error, data)

  if (isPending) {
    return "Loading..."
  }

  return <>
    <POIUnitCard
      team={currentPlayer.fullTeamName.default}
      isPlayerMatchPOIU={true}
      isSimilarMatchPOIU={false}
      unitId={currentPlayerPOIU}
    />
  </>
}