
import PlayerSearchInput from "@/components/player/PlayerSearchInput";

import PlayerMatchPOIUSection from '@/components/poiu/PlayerMatchPOIUSection'
import SimilarPOIUSection from "@/components/poiu/SimilarPOIUSection";
import SituationTabs from "@/components/controls/SituationTabs";
export default function Home() {




  return (
    <div className="container mx-auto py-6 px-4">
      <h1 className="text-3xl font-bold text-center mb-8">NHL Player On Ice Unit (POIU) Comparison Tool</h1>
      <PlayerSearchInput />
      <SituationTabs />


      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <PlayerMatchPOIUSection />
        <SimilarPOIUSection />
      </div>

    </div>
  );
}
