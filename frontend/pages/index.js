
import PlayerSearchInput from "@/components/player/PlayerSearchInput";
import POIUnitCard from "@/components/poiu/POIUnitCard"
import SituationTabs from "@/components/controls/SituationTabs";
export default function Home() {
  return (
    <div className="container mx-auto py-6 px-4">
      <h1 className="text-3xl font-bold text-center mb-8">NHL Player On Ice Unit (POIU) Comparison Tool</h1>
      <PlayerSearchInput />
      <SituationTabs />

      {/* Just removing the tabs cards for testing  */
        false &&
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <POIUnitCard
            title={`Connor Mcdavid's most common POIU`}
            team={"Edmonton Oilers"}
          />
          <POIUnitCard
            title={`Best POIU Comparable`}
            team={"Toronto Maple Leafs"}
          />
        </div>
      }

    </div>
  );
}
