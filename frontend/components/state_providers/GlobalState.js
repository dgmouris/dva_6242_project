import {createContext, useContext, useState} from 'react'


export const GlobalState = createContext({})


export const useGlobalState = function () {
  const globalState = useContext(GlobalState)
  return globalState
}


export default function GlobalStateProvider({children}) {
  // this will set in search and used elsewhere.
  const [currentPlayer, setCurrentPlayer] = useState()

  // default is 5on5, set in Situation tabs.
  const [currentSituation, setCurrentSituation] = useState("5on5")

  // match set to first POIU.
  const [currentPlayerPOIU, setCurrentPlayerPOIU] = useState()
  // list of player match POIUs
  const [allPlayerMatchPOIUs, setAllPlayerMatchPOIUs] = useState([])
  // state for similar POIUs
  const [currentSimilarPOIU, setCurrentSimilarPOIU] = useState()
  // list of similiar POIU ids.
  const [allSimilarPOIUs, setAllSimilarPOIUs] = useState([])

  return <GlobalState.Provider value={{
    currentPlayer, setCurrentPlayer,
    currentSituation, setCurrentSituation,
    currentPlayerPOIU, setCurrentPlayerPOIU,
    allPlayerMatchPOIUs, setAllPlayerMatchPOIUs,
    currentSimilarPOIU, setCurrentSimilarPOIU,
    allSimilarPOIUs, setAllSimilarPOIUs,
  }}>
    {children}
  </GlobalState.Provider>
}