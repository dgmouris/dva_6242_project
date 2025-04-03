
import {
  Tabs,

  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"

import { useGlobalState } from "../state_providers/GlobalState"


export default function SituationTabs() {

  const {currentSituation, setCurrentSituation} = useGlobalState()


  return <div className="w-full mb-2 flex justify-center">
     <h1 className="text-xl font-bold text-center mb-8 mr-3">POIU Situation</h1>
    <Tabs defaultValue="5on5" className="w-[400px]"
      value={currentSituation}
      onValueChange={setCurrentSituation}
    >
      <TabsList className="grid text-center grid-cols-4"

      >
        <TabsTrigger value="5on5">5 on 5</TabsTrigger>
        <TabsTrigger value="5on4">PowerPlay </TabsTrigger>
        <TabsTrigger value="4on5">Penalty Kill</TabsTrigger>
      </TabsList>
    </Tabs>
  </div>
}