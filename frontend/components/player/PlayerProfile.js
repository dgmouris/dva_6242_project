import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

import { Badge } from "@/components/ui/badge"

import {
  useQuery,
} from '@tanstack/react-query'

const longPosition = (oneCharValue) => {
  if (oneCharValue === "C") return "Center"
  if (oneCharValue === "L") return "Left Wing"
  if (oneCharValue === "R") return "Right Wing"
  if (oneCharValue === "D") return "Defense"
}

// takes in the id of the player based on nhl.com's id
export default function PlayerProfile ({playerId}) {
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

  if (isPending) return 'Loading...'

  if (error) return 'An error has occurred: ' + error.message

  const playerName = `${data.firstName.default} ${data.lastName.default}`

  console.log(data)
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
