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

  let { isPending, error, data, refetch } = useQuery({
    queryKey: [`search-results`],
    queryFn: async ()=> {
      return await searchPlayers({name: searchQuery})
    },
    enabled: searchQuery.length >= 3,
    staleTime: Infinity,
  })

  const handleSearch = async () => {

  }
  useEffect(()=> {
    if (searchQuery.length >= 3) {
      // const data = await searchPlayers({name: searchQuery})
      refetch()
      console.log(data)
      if (data) {
        setSearchResults(data.players)
      }
      // this is from the api backend
    } else {
      setSearchResults([])
    }

  }, [searchQuery])

  if (isPending) {
    return "Loading ..."
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
        {
          searchResults.map((player)=> {
            console.log(player)
            return <PlayerProfile
              key={player.id}
              isSearchResult={true}
              playerId={player.id}
            />
          })
        }
      </div>
    </div>
  </div>
}