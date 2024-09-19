<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" required>
      <input v-model="password" type="password" placeholder="Password" required>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const username = ref('')
    const password = ref('')

    const login = async () => {
      try {
        await api.login(username.value, password.value)
        router.push('/dashboard')
      } catch (error) {
        console.error('Login failed:', error)
      }
    }

    return { username, password, login }
  }
}
</script>