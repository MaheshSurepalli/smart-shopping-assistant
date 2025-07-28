import { useState, useEffect, useRef } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import ReactMarkdown from 'react-markdown'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [shouldAutoScroll, setShouldAutoScroll] = useState(true)

  const { loginWithRedirect, logout, isAuthenticated, user, getAccessTokenSilently } = useAuth0()
  const chatBoxRef = useRef(null)
  const bottomRef = useRef(null)

  // Load chat history after login
  useEffect(() => {
    const fetchMessages = async () => {
      if (!isAuthenticated) return
      try {
        const token = await getAccessTokenSilently()
        const res = await fetch('http://localhost:8000/messages', {
          headers: { Authorization: `Bearer ${token}` },
        })
        const data = await res.json()
        setMessages(data.messages.map(msg => ({
          role: msg.role === 'User' ? 'You' : msg.role,
          text: msg.text,
        })))

        setShouldAutoScroll(true)
      } catch (err) {
        console.error("Failed to load history", err)
      }
    }
    fetchMessages()
  }, [isAuthenticated])

  // Smart scroll to bottom
  useEffect(() => {
    if (shouldAutoScroll && bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, shouldAutoScroll])

  const sendMessage = async () => {
    if (!input.trim()) return
    const userMsg = { role: 'You', text: input }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)
    setShouldAutoScroll(true)

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

  const handleScroll = () => {
    if (!chatBoxRef.current) return
    const { scrollTop, scrollHeight, clientHeight } = chatBoxRef.current
    const atBottom = scrollHeight - scrollTop - clientHeight < 50
    setShouldAutoScroll(atBottom)
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-inner">
          <h2>🛒 Smart Shopping Assistant</h2>
          {isAuthenticated && (
            <div className="user-info">
              <span>Hello, {user?.name}</span>
              <button onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}>
                🔓 Logout
              </button>
            </div>
          )}
        </div>
      </header>


      <main className="chat-container">
        {!isAuthenticated ? (
          <div className="centered-login">
            <button onClick={() => loginWithRedirect()}>🔐 Login with Auth0</button>
          </div>
        ) : (
          <>
            <div className="chat-box" ref={chatBoxRef} onScroll={handleScroll}>
              {messages.map((msg, i) => (
                <div key={i} className={`msg ${msg.role.toLowerCase()}`}>
                  <div className="bubble">
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                  </div>
                </div>
              ))}
              <div ref={bottomRef} />
            </div>

            <div className="input-box">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask anything..."
              />
              <button onClick={sendMessage} disabled={loading}>
                {loading ? '...' : '➤'}
              </button>
            </div>
          </>
        )}
      </main>
    </div>
  )
}

export default App
