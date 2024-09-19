<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" required>
      <input v-model="password" type="password" placeholder="Password" required>
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

export default {
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const username = ref('')
    const password = ref('')

    const register = async () => {
      try {
        await api.register(username.value, password.value)
        router.push('/login')
      } catch (error) {
        console.error('Registration failed:', error)
      }
    }

    return { username, password, register }
  }
}
</script>