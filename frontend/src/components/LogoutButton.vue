<template lang="pug">
  v-btn(
    v-if="this.$store.getters.isAuthenticated"
    depressed dark small color="blue-grey darken-3"
    @click.prevent="logout"
  )
    | Выйти
    v-icon.ml-2 input
</template>

<script lang="ts">
// Imports
import Vue from 'vue';
import AUTH from '@/store/actions/auth';

export default Vue.extend({
  data:() => ({}),
  methods: {
    logout() {
      this.$store.dispatch(AUTH.LOGOUT)
        .then(() => {
          this.$router.push('/login');
        })
        .catch((error) => {
          // console.log(error);
        });
    },
  },
});
</script>
