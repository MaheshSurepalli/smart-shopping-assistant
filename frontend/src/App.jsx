import { useState } from 'react'
import './App.css'
import { useAuth0 } from '@auth0/auth0-react'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const { loginWithRedirect, logout, isAuthenticated, user, getAccessTokenSilently } = useAuth0()

  const sendMessage = async () => {
    if (!input.trim()) return
    const userMsg = { role: 'You', text: input }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const token = await getAccessTokenSilently()
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ message: input }),
      })

      const data = await res.json()
      const botMsg = { role: 'Assistant', text: data.reply }
      setMessages((prev) => [...prev, botMsg])
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'Assistant', text: 'Error: could not connect.' }])
    }

    setLoading(false)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') sendMessage()
  }

  return (
    <div className="app">
      <h2>🛒 Smart Shopping Assistant</h2>

      {!isAuthenticated ? (
        <div style={{ textAlign: 'center' }}>
          <button onClick={() => loginWithRedirect()}>🔐 Login with Auth0</button>
        </div>
      ) : (
        <>
          <div style={{ textAlign: 'right' }}>
            <span>Welcome, {user?.name} </span>
            <button onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}>
              Logout
            </button>
          </div>

          <div className="chat-box">
            {messages.map((msg, i) => (
              <div key={i} className={`msg ${msg.role.toLowerCase()}`}>
                <strong>{msg.role}:</strong> {msg.text}
              </div>
            ))}
          </div>

          <div className="input-box">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask something..."
            />
            <button onClick={sendMessage} disabled={loading}>Send</button>
          </div>
        </>
      )}
    </div>
  )
}

export default App
