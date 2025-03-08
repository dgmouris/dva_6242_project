import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

import PlayerProfile from "../player/PlayerProfile"


export default function POIUnitCard({title, team}) {

  return <Card className="border-t-8">
    <CardHeader
      className="flex flex-col items-center justify-between pb-2"

    >
      <div className="text-center">

        <CardTitle>{title}</CardTitle>
        <CardDescription>{team}</CardDescription>
      </div>
      {/* forwards handle if it's 4 */}
      <div className="flex items-center w-full justify-between gap-2">
        <PlayerProfile
          playerName={"connor mcdavid"}
          number={97}
          position={"Center"}
          imageUrl={"https://assets.nhle.com/mugs/nhl/20242025/EDM/8478402.png"}
          badgeColor={"blue"}
        />
        <PlayerProfile
          playerName={"connor mcdavid"}
          number={97}
          position={"Center"}
          imageUrl={"https://assets.nhle.com/mugs/nhl/20242025/EDM/8478402.png"}
          badgeColor={"blue"}
        />
        <PlayerProfile
          playerName={"connor mcdavid"}
          number={97}
          position={"Center"}
          imageUrl={"https://assets.nhle.com/mugs/nhl/20242025/EDM/8478402.png"}
          badgeColor={"blue"}
        />
      </div>
      {/* defensemen */}
      <div className="flex items-center w-3/5 justify-between gap-2">
        <PlayerProfile
          playerName={"connor mcdavid"}
          number={97}
          position={"Center"}
          imageUrl={"https://assets.nhle.com/mugs/nhl/20242025/EDM/8478402.png"}
          badgeColor={"blue"}
        />
        <PlayerProfile
          playerName={"connor mcdavid"}
          number={97}
          position={"Center"}
          imageUrl={"https://assets.nhle.com/mugs/nhl/20242025/EDM/8478402.png"}
          badgeColor={"blue"}
        />
      </div>
    </CardHeader>

  </Card>
}