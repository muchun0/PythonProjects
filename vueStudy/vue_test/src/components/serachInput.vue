<template>
    <div>
        <input type="text" v-model="keyWord" placeholder="Search" @keyup.enter="search"/>
    </div> 
</template>

<script>
import axios from 'axios';
export default {
    name: 'searchInput',
    data() {
        return {
            keyWord: ''
        }
    },
    methods: {
        search() {
            axios.get('https://api.github.com/search/users?q=' + this.keyWord)
                .then(response => {
                    // this.$emit('search', response.data.items);
                    console.log(response.data.items);
                })
                .catch(error => {
                    console.log(error);
                })
        }}}
</script>

<style>

</style>