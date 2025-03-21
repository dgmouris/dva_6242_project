import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

import PlayerProfile from "../player/PlayerProfile"
import POIUnitAnalysis from "./POIUnitAnalysis"


export default function POIUnitCard({title, team, id}) {

  const DUMMY_UNITS = [
    "Unit: 1",
    "Unit: 2",
    "Unit: 3",
    "Unit: 4",
    "Unit: 5"
  ]

  return <Card className="border-t-8">
    <CardHeader
      className="flex flex-col items-center justify-between pb-2"
    >
      <div className="flex w-full mb-2">
        <div className="text-center flex-1">
          <CardTitle>{title}</CardTitle>
          <CardDescription>{team}</CardDescription>
        </div>
        {/* Units will have to be changed a bit differently */}
        <Select className="flex-none" value={""} onValueChange={()=>{}}>
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="Select different POIU" />
          </SelectTrigger>
          <SelectContent>
            {DUMMY_UNITS.map((dummyUnit, index)=> {

               return <SelectItem key={dummyUnit} value={dummyUnit}>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" />
                  {dummyUnit}
                </div>
              </SelectItem>
            })}
          </SelectContent>
        </Select>

      </div>
      {/* forwards handle if it's 4 */}
      <div className="flex items-center w-full justify-between gap-2">
        <PlayerProfile
          playerId={8475786}
        />
        <PlayerProfile
          playerId={8478402}
        />
        <PlayerProfile
          playerId={8479318}
        />
      </div>
      {/* defensemen */}
      <div className="flex items-center w-3/5 justify-between gap-2">
        <PlayerProfile
          playerId={8480803}
        />
        <PlayerProfile
          playerId={8475218}
        />
      </div>
    </CardHeader>
    <CardContent>
      <POIUnitAnalysis id={id}/>
    </CardContent>
  </Card>
}