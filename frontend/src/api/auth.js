import { defineStore } from 'pinia'
import apiClient from '@/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    userProfile: null,
    loading: false,
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.userProfile?.role_name === 'admin',
    isCitizen: (state) => state.userProfile?.role_name === 'citizen',
  },
  
  actions: {
    async login(credentials) {
      try {
        this.loading = true
        const response = await apiClient.post('api/token/', credentials)
        
        // Stocker les tokens
        this.token = response.data.access
        this.refreshToken = response.data.refresh
        
        localStorage.setItem('token', this.token)
        localStorage.setItem('refreshToken', this.refreshToken)
        
        // Charger le profil de l'utilisateur
        await this.fetchUserProfile()
        router.push('/dashboard')
        
        return true
      } catch (error) {
        console.error('Login error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async register(userData) {
      try {
        this.loading = true
        await apiClient.post('api/register/', userData)
        return true
      } catch (error) {
        console.error('Register error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchUserProfile() {
      try {
        const response = await apiClient.get('api/profile/')
        this.userProfile = response.data
        
        // Mettre à jour l'utilisateur dans le state et localStorage
        this.user = {
          ...response.data,
          token: this.token,
          refreshToken: this.refreshToken
        }
        
        localStorage.setItem('user', JSON.stringify(this.user))
        return this.userProfile
      } catch (error) {
        console.error('Fetch profile error:', error)
        throw error
      }
    },
    
    async refreshToken() {
      try {
        if (!this.refreshToken) return false
        
        const response = await apiClient.post('api/token/refresh/', {
          refresh: this.refreshToken
        })
        
        this.token = response.data.access
        localStorage.setItem('token', this.token)
        
        // Mettre à jour l'utilisateur si existant
        if (this.user) {
          this.user = { ...this.user, token: this.token }
          localStorage.setItem('user', JSON.stringify(this.user))
        }
        
        return true
      } catch (error) {
        this.logout()
        throw error
      }
    },
    
    async updateProfile(userData) {
      try {
        this.loading = true
        const response = await apiClient.put('api/profile/', userData)
        this.userProfile = response.data
        
        // Mettre à jour l'utilisateur dans le localStorage
        this.user = { ...this.user, ...response.data }
        localStorage.setItem('user', JSON.stringify(this.user))
        
        return this.userProfile
      } catch (error) {
        console.error('Update profile error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      this.refreshToken = null
      this.userProfile = null
      
      localStorage.removeItem('user')
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      
      router.push('/login')
    }
  }
})
