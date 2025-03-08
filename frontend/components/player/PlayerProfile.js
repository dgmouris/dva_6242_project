import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

import { Badge } from "@/components/ui/badge"


export default function PlayerProfile ({playerName, number, position, imageUrl}) {
  return <>
    <div className="flex items-center justify-between mb-2">
      <div className="flex flex-col items-center gap-2">
        <Avatar className="h-20 w-20 border">
          <AvatarImage src={imageUrl} alt={playerName} />
          <AvatarFallback>
            {playerName}
          </AvatarFallback>
        </Avatar>
        <div>
          <div className="font-medium flex items-center gap-1">
            {playerName}
          </div>
        </div>
        <Badge variant="outline">{position} #{number}</Badge>
      </div>
    </div>
  </>
}
