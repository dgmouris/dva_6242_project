import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

import POIUnitAnalysis from "./POIUnitAnalysis"
import POIUPlayerProfiles from './POIUPlayerProfiles'
import { useGlobalState } from '../state_providers/GlobalState'


// this component is used on both similar matches and player match poius.
export default function POIUnitCard({unitId, team, isPlayerMatchPOIU, isSimilarMatchPOIU}) {

  const {
    currentPlayer,
    currentPlayerPOIU,
    currentSimilarPOIU,
    setCurrentPlayerPOIU,
    setCurrentSimilarPOIU,
    allPlayerMatchPOIUs,
    allSimilarPOIUs,
  } = useGlobalState()

  let units  = []
  // using the same card for player match and similarities
  if (isPlayerMatchPOIU) {
    units = allPlayerMatchPOIUs
  } else if (isSimilarMatchPOIU) {
    units = allSimilarPOIUs
  }

  // sets the current poiu for player match and similarities
  const handleUnitChange = (value) => {
    if (isPlayerMatchPOIU) {
      setCurrentPlayerPOIU(value)
    } else if (isSimilarMatchPOIU) {
      setCurrentSimilarPOIU(value)
    }
  }

  // just used for titles.
  let unitAsRankForTitle = allPlayerMatchPOIUs.indexOf(currentPlayerPOIU)+1
  let fullName = ""
  if (currentPlayer) {
    fullName = `${currentPlayer.firstName.default} ${currentPlayer.lastName.default}`
  }
  // current unit is used for all of the analytics tables and charts
  // essentially we'll be fetching the data based on this.
  let currentUnit
  let title
  if (isPlayerMatchPOIU) {
    currentUnit = currentPlayerPOIU
    title=`${fullName}'s POIU best match ${unitAsRankForTitle}`
  } else if (isSimilarMatchPOIU) {
    currentUnit = currentSimilarPOIU
    title=`Similar POIUs to ${fullName} best match ${unitAsRankForTitle}`
  }

  if (!currentUnit) {
    return <></>
  }

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
        <Select className="flex-none" value={""} onValueChange={handleUnitChange}>
          <SelectTrigger className="w-[200px]">
            <SelectValue placeholder="Select different POIU" />
          </SelectTrigger>
          <SelectContent>
            {units?.map((unit, index)=> {
               return <SelectItem key={unit} value={unit}>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" />
                  Best unit match {index+ 1}
                </div>
              </SelectItem>
            })}
          </SelectContent>
        </Select>
      </div>
      {/* forwards handle if it's 4 */}
      <POIUPlayerProfiles unitId={unitId}/>
    </CardHeader>
    <CardContent>
      <POIUnitAnalysis id={unitId}/>
    </CardContent>
  </Card>
}