import {useEffect} from 'react'
import {
  useQuery,
  useQueryClient
} from '@tanstack/react-query'

import PlayerProfile from "../player/PlayerProfile"

import { useGlobalState } from "../state_providers/GlobalState"

import { getPlayersByPoiu } from '@/utils/api/players'

// this is just going to show the head shots.
export default function POIUPlayerProfiles({unitId}) {
  const queryClient = useQueryClient();
  const {
    currentPlayerPOIU
  } = useGlobalState()
  const queryKey = `all-player-profiles-${unitId}`

  let { isLoading, error, data, refetch } = useQuery({
    queryKey: [queryKey],
    queryFn: async () => {
      return await getPlayersByPoiu({poiuId: unitId})
    },
    enabled: false, // this will only fetch once you get a player
    staleTime: Infinity,
  })

  useEffect(()=> {
    if (!unitId) return // guard
    queryClient.invalidateQueries(queryKey)
    refetch()
  },[currentPlayerPOIU, unitId])

  if (isLoading) {
    return "Loading profiles..."
  }

  if (!data) {
    return <></>
  }

  return <>
    {/* Forwards */}
    <div className="flex items-center w-full justify-between gap-2">

      {data.forwards?.map((player)=> {
        return <PlayerProfile
          key={player.id}
          playerId={player.id}
        />
      })}
    </div>
    {/* defensemen */}
    <div className="flex items-center w-3/5 justify-between gap-2">
      {data.defensemen?.map((player)=> {
        return <PlayerProfile
          key={player.id}
          playerId={player.id}
        />
      })}
    </div>
  </>
}