const ProfileCard = ({ profile, onVote, revealed }) => {
    return (
      <div className="flex flex-col items-center border rounded-xl shadow p-4 w-64 transition hover:scale-105">
        <img
          src={profile.image_url}
          className="w-32 h-32 object-cover rounded-full mb-4"
        />
        <h2 className="text-lg font-semibold">
          {revealed ? `ID: ${profile.id}` : 'Anonymous'}
        </h2>
        <div className="text-sm text-gray-600 mt-2">
          {profile.education?.[0] ?? 'No education listed'}
        </div>
        <button
          className="mt-4 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-full"
          onClick={() => onVote(profile.id)}
        >
          Vote
        </button>
      </div>
    )
  }
  
  export default ProfileCard
  