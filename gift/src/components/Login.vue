<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="onSubmit">
      <input type="text" v-model="form.username" placeholder="Name" />
      <input type="password" v-model="form.password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'

// do not use same name with ref
const form = reactive({
  username: '',
  password: '',
})

const onSubmit = () => {
  console.log('submit!')
  //请求登录接口
  //登录成功后，跳转到首页
  // this.$router.push('/')
  
}
</script>
