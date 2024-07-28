import React, { useState } from "react";
import "./Links.css";

export default function Links() {
  const [spotifyLink, setSpotifyLink] = useState("");
  const [playlistDetails, setPlaylistDetails] = useState(null);

  function getSpotifyID() {
    const playlistID = spotifyLink.substring(34, 56);
    console.log("Spotify Playlist Link:", playlistID);
    return playlistID;
  }

  function copy() {
    const spotifyID = getSpotifyID();
    getPlaylist(spotifyID);
  }

  async function getPlaylist(spotifyID) {
    const accessToken = process.env.REACT_APP_SPOTIFY_ACCESS_TOKEN;
    const response = await fetch(
      `https://api.spotify.com/v1/playlists/${spotifyID}/tracks`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (response.ok) {
      const playlist = await response.json();
      console.log("Playlist Details:", playlist);

      const trackNames = playlist.items.map((item) => item.track.name);
      console.log("Track Names:", trackNames);

      setPlaylistDetails(trackNames);
    } else {
      console.error(
        "Failed to fetch playlist:",
        response.status,
        response.statusText
      );
    }
  }

  return (
    <div className="container">
      <div id="spotify">
        <div className="caption">Enter a Spotify Playlist Link</div>
        <input
          id="SpotifyLink"
          type="text"
          placeholder="https://open.spotify.com/playlist/{playlist_id}?si=aa798b34a9594e53"
          value={spotifyLink}
          onChange={(e) => setSpotifyLink(e.target.value)}
        />
      </div>
      <div id="youtube">
        <div className="caption">Enter a Youtube Playlist Link</div>
        <input
          id="YoutubeLink"
          type="text"
          placeholder="https://www.youtube.com/playlist?list=PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10"
        />
      </div>
      <div id="submit">
        <button id="submitBtn" onClick={copy}>
          Copy to Youtube
        </button>
      </div>
      {playlistDetails && (
        <div id="playlistDetails">
          {playlistDetails.map((track, index) => (
            <div key={index} className="track-name">
              {track}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
