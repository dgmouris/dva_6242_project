import {BASE_URL} from './base'

export async function  searchPlayers({name}) {
  const response = await fetch(`${BASE_URL}/search_players?q=${name}`)
  const data = await response.json()
  return data
}

export async function getUnitsByPlayerId({playerId, situation}) {
  const response = await fetch(`${BASE_URL}/get_units_by_player_id?player_id=${playerId}&situation=${situation}`)
  const data = await response.json()
  return data
}

export async function getPlayersByPoiu({poiuId}) {
  const response = await fetch(`${BASE_URL}/get_players_by_poiu?poiu=${poiuId}`)
  const data = await response.json()
  return data
}

export async function getSimilarUnitsByPoiu({ poiuId, situation }) {
  const response = await fetch(`${BASE_URL}/get_similar_units_by_poiu?poiu=${poiuId}&situation=${situation}`)
  const data = await response.json()
  return data
}
