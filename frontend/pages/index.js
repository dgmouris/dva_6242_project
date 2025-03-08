
import PlayerSearchInput from "@/components/PlayerSearchInput";

export default function Home() {
  return (
    <div className="container mx-auto py-6 px-4">
      <h1 className="text-3xl font-bold text-center mb-8">NHL Player On Ice Unit Comparison Tool</h1>

      <PlayerSearchInput />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      </div>

    </div>
  );
}
