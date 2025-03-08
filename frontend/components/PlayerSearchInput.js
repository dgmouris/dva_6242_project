import {useState} from 'react'

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

// maybe this should be in a
export default function PlayerSearchInput () {
  const [searchQuery, setSearchQuery] = useState("")

  const handleSearch = () => {

  }

  return <div className="w-full max-w-3xl mx-auto p-4">
    <div className="flex flex-col space-y-4">
      <h1 className="text-2xl font-bold">NHL Player Search</h1>

      <div className="flex w-full items-center space-x-2">
        <div className="relative flex-1">
          <Input
            type="text"
            placeholder="Search by player name"
            className="pl-8"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          />
        </div>
        <Button onClick={handleSearch}>Search</Button>
      </div>
    </div>
  </div>
}