import {BASE_URL} from './base'

export async function  searchPlayers({name}) {
  const response = await fetch(`${BASE_URL}/search_players?q=${name}`)
  const data = await response.json()
  return data
}
