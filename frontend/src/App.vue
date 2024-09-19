<template>
  <nav>
    <router-link to="/dashboard">Dashboard</router-link>
    <router-link to="/login">Login</router-link>
    <router-link to="/register">Register</router-link>
    <a @click="logout" v-if="isLoggedIn">Logout</a>
  </nav>
  <router-view/>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from './api'

export default {
  name: 'app',
  setup() {
    const router = useRouter()
    const isLoggedIn = ref(false)

    onMounted(() => {
      isLoggedIn.value = !!localStorage.getItem('token')
    })

    const logout = () => {
      api.logout()
      isLoggedIn.value = false
      router.push('/login')
    }

    return { isLoggedIn, logout }
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
