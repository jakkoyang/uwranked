import React, { useEffect, useState } from 'react'
import axios from 'axios'
import ProfileCard from '../components/ProfileCard'

const MatchPage = () => {
  const [profiles, setProfiles] = useState([])
  const [revealed, setRevealed] = useState(false)

  const loadProfiles = () => {
    axios.get('http://localhost:8000/match').then(res => {
      setProfiles(res.data)
      setRevealed(false)
    })
  }

  useEffect(() => {
    loadProfiles()
  }, [])

  const handleVote = (winnerId) => {
    const loserId = profiles.find(p => p.id !== winnerId)?.id
    axios.post('http://localhost:8000/vote', null, {
      params: {
        winner_id: winnerId,
        loser_id: loserId,
      },
    }).then(() => {
      setRevealed(true)
      setTimeout(loadProfiles, 1500)
    })
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8">
      <h1 className="text-3xl font-bold mb-8">Who's More Cracked?</h1>
      <div className="flex gap-8">
        {profiles.map((p) => (
          <ProfileCard key={p.id} profile={p} onVote={handleVote} revealed={revealed} />
        ))}
      </div>
    </div>
  )
}

export default MatchPage
