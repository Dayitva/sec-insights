/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unsafe-argument */
/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
import { createContext, useState, useEffect } from 'react'
import netlifyIdentity from 'netlify-identity-widget'

interface User {
  app_metadata?: {
    roles?: string[];
  };
  // other properties...
}

const AuthContext = createContext<{ user: User | null, login: () => void, logout: () => void, authReady: boolean }>({
  user: null,
  login: () => { console.log('login method') },
  logout: () => { console.log('logout method') },
  authReady: false
})

export const AuthContextProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState(null)
  const [authReady, setAuthReady] = useState(false)

  useEffect(() => {
    netlifyIdentity.on('login', (user: any) => {
      setUser(user)
      netlifyIdentity.close()
      console.log('login event')
    })
    netlifyIdentity.on('logout', () => {
      setUser(null)
      console.log('logout event')
    })
    netlifyIdentity.on('init', (user: any) => {
      setUser(user)
      setAuthReady(true)
      console.log('init event')
    })

    // init netlify identity connection
    netlifyIdentity.init()

    return () => {
      netlifyIdentity.off('login')
    }
  }, [])

  const login = () => {
    netlifyIdentity.open()
  }

  const logout = () => {
    void netlifyIdentity.logout()
  }

  const context = { user, login, logout, authReady }

  return (
    <AuthContext.Provider value={context}>
      { children }
    </AuthContext.Provider>
  )
}

export default AuthContext