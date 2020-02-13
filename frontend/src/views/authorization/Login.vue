<template lang="pug">
  v-container.pa-0(fluid fill-height)
    v-row(no-gutters align="center" justify="center")
      v-card(flat width="400px")
        v-toolbar(flat dark color="blue-grey darken-3")
          v-toolbar-title Вход в систему
          v-spacer
          v-icon people

        v-form(@submit.prevent="login")
          v-text-field(
            filled
            v-model="email"
            label="Логин"
            hide-details
          )
          v-text-field(
            filled
            v-model="password"
            label="Пароль"
            type="password"
            counter
            hide-details
          )
          .px-2.py-4.text-right
            v-btn.mx-2(
              depressed dark
              color="blue-grey darken-3"
              type="submit"
            ) Войти
</template>

<script lang="ts">
// Imports
import Vue from 'vue';
import AUTH from '@/store/actions/auth';

export default Vue.extend({
  props: {
    appBar: {
      type: Boolean,
      default: false as boolean,
    },
    navigationDrawer: {
      type: Boolean,
      default: false as boolean,
    },
  },
  data:() => ({
    email: '' as string,
    password: '' as string,
  }),
  watch: {
    appBar: {
      handler(value: boolean) {
        this.$emit('setAppBarValue', value);
      },
      immediate: true,
    },
    navigationDrawer: {
      handler(value: boolean) {
        this.$emit('setNavigationDrawerValue', value);
      },
      immediate: true,
    },
  },
  methods: {
    login() {
      const { password, email } = this;
      this.$store.dispatch(AUTH.REQUEST, { password, email })
        .then(() => {
          this.$router.push('/');
          this.$emit('setAppBarValue', true);
          this.$emit('setNavigationDrawerValue', true);
        })
        .catch((error) => {
          // console.log(error);
        });
    },
  },
});
</script>
