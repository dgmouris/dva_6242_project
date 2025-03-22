import {
  useQuery,
} from '@tanstack/react-query'

import { Card, CardContent } from "@/components/ui/card"

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

import { Badge } from "@/components/ui/badge"

import { useGlobalState } from '../state_providers/GlobalState'


const longPosition = (oneCharValue) => {
  if (oneCharValue === "C") return "Center"
  if (oneCharValue === "L") return "Left Wing"
  if (oneCharValue === "R") return "Right Wing"
  if (oneCharValue === "D") return "Defense"
}

// takes in the id of the player based on nhl.com's id
export default function PlayerProfile ({playerId, isSearchResult, clearSearch}) {
  const {currentPlayer, setCurrentPlayer} = useGlobalState()

  const { isPending, error, data } = useQuery({
    queryKey: [`player-${playerId}`],
    queryFn: async () => {
      const URL = `/api/player?playerId=${playerId}`
      const response = await fetch(URL)
      const data = await response.json()
      return data
    },
    staleTime: Infinity,
  })

  // this is to select the player
  const selectPlayer = () => {
    // sets the player to the current object
    setCurrentPlayer(data)
    clearSearch()
  }

  if (isPending) return 'Loading...'

  if (error) return 'An error has occurred: ' + error.message

  const playerName = `${data.firstName.default} ${data.lastName.default}`

  if (isSearchResult) {
    if (!data) {
      return <></>
    }
    return  <Card
      key={playerId} className="overflow-hidden"
      onClick={selectPlayer}
    >
      <CardContent className="p-4">
        <div className="flex items-center space-x-4">
          <Avatar>
            <AvatarImage src={data.headshot} alt={playerName} />
            <AvatarFallback>{playerName.substring(0, 2)}</AvatarFallback>
          </Avatar>

          <div className="flex-1 space-y-1">
            <div className="flex  items-center justify-between">
              <p className="text-sm grow-1 font-medium leading-none">
                {playerName} <span className="text-muted-foreground">#{data.sweaterNumber}</span>
              </p>
              <p className="flex text-sm text-muted-foreground">{data.fullTeamName?.default}</p>
              <div className="rounded-full bg-primary/10 px-2 py-1 text-xs font-medium text-primary">
                {data.position}
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  }

  return <>
    <div className="flex items-center justify-between mb-2">
      <div className="flex flex-col items-center gap-2">
        <Avatar className="h-20 w-20 border">
          <AvatarImage src={data.headshot} alt={playerName} />
          <AvatarFallback>
            {playerName}
          </AvatarFallback>
        </Avatar>
        <div>
          <div className="font-medium flex items-center gap-1">
            {playerName}
          </div>
        </div>
        <Badge variant="outline">{longPosition(data.position)} #{data.sweaterNumber}</Badge>
      </div>
    </div>
  </>
}
