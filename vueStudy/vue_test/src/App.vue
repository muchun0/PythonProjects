<template>
    <div>
        <searchInput></searchInput>
        <userList></userList>
    </div>
</template>

<script>
import searchInput from './components/serachInput.vue';
import userList from './components/userList.vue';

export default {
  name: 'App',
  components: {searchInput,userList},
}
</script>

<style>

</style>
