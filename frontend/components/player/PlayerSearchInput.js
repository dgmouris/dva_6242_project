import {useState, useEffect} from 'react'

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

import PlayerProfile from './PlayerProfile'

import { searchPlayers } from '@/utils/api/players'



import {
  useQuery,
} from '@tanstack/react-query'

// maybe this should be in a
export default function PlayerSearchInput () {
  const [searchQuery, setSearchQuery] = useState("")
  const [searchResults, setSearchResults] = useState([])

  // this is all for the search
  let { isPending, error, data, refetch } = useQuery({
    queryKey: [`search-results`],
    queryFn: async ()=> {
      return await searchPlayers({name: searchQuery})
    },
    enabled: searchQuery.length >= 3,
    staleTime: Infinity,
  })
  const handleSearch =  () => {
    if (searchQuery.length >= 3) {
      // const data = await searchPlayers({name: searchQuery})
      refetch()
      if (data) {
        setSearchResults(data.players)
      }
      // this is from the api backend
    } else {
      setSearchResults([])
    }
  }
  useEffect(()=> {
    handleSearch()
  }, [searchQuery])
  // end the search section

  // pass this down to clear the search once user selects it.
  const clearSearch = () => {
    setSearchQuery("")
    setSearchResults([])
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
      <div className="space-y-3">
        { searchResults &&
          searchResults.map((player)=> {
            if (!player) return
            return <PlayerProfile
              key={player.id}
              playerId={player.id}
              // these two are only for search.
              isSearchResult={true}
              clearSearch={clearSearch}
            />
          })
        }
      </div>
    </div>
  </div>
}