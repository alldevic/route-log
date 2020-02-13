<template lang="pug">
  v-app
    v-navigation-drawer(
      v-if="navDrawer"
      app dark
      color="blue-grey darken-3"
      v-model="drawer"
      width="320"
    )
      v-list.pb-0(subheader)
        v-list-item
          v-list-item-content
            v-list-item-title
              h4 Экотек
            v-list-item-subtitle.caption Маршрутный журнал

      v-list
        v-list-item
          v-list-item-content
            v-menu(
              v-model="datePickerMenu"
              transition="scroll-y-transition"
              offset-y
              max-width="290px"
              min-width="290px"
            )
              template(v-slot:activator="{ on }")
                v-text-field(
                  v-model="date"
                  clearable
                  label="Выберите дату"
                  prepend-icon="event"
                  v-on="on"
                )
              v-date-picker(
                v-model="date"
                no-title
                @input="datePickerMenu = false"
              )
        v-divider(v-if="date")
        v-list-item
          v-list-item-content
            v-file-input(
              v-model="attachment"
              show-size
              counter
              :label="fileTypesDict[fileTypes.attachment].label"
              @change.sync="onUploadFiles({ file: $event, id: 1 })"
            )
        v-list-item
          v-list-item-content
            v-file-input(
              v-model="application"
              show-size
              counter
              :label="fileTypesDict[fileTypes.application].label"
              @change.sync="onUploadFiles({ file: $event, id: 1 })"
            )
        v-divider(v-if="application || attachment")
        v-list-item(v-if="application || attachment")
          v-list-item-content
            v-autocomplete(
              v-model="selectedDevice"
              :items="devices"
              :search-input.sync="searchDevice"
              item-text="name"
              item-value="id"
              hide-no-data
              clearable
              label="Выберите автомобиль"
              prepend-icon="directions_car"
            )
        v-list-item
          v-list-item-content
            v-btn(
              @click="createReport"
              color="primary"
              depressed
              :disabled="!selectedDevice"
            ) Сформировать отчет

    v-app-bar(
      v-if="appBar"
      app dark flat
      color="blue-grey darken-3"
    )
      v-app-bar-nav-icon(@click.stop="drawer = !drawer")
      v-spacer
      logout-button

    v-content(:style="{ '--appTopHeight': appTopHeight }")
      router-view(
        @setAppBarValue="onSetAppBarValue"
        @setNavigationDrawerValue="onSetNavigationDrawerValue"
      )
</template>

<script lang="ts">
import Vue from "vue";
import LogoutButton from "@/components/LogoutButton.vue";
import Repository from "@/api/Repository";
import RepositoryFactory from "@/api/RepositoryFactory";
import AUTH from "./store/actions/auth";
import FILE_TYPES from "@/constants/fileTypes";
import FILE_TYPES_DICT from "@/dictionaries/fileTypesDict";

const DevicesRepository = RepositoryFactory.get("devices");
const ReportsRepository = RepositoryFactory.get("reports");

export default Vue.extend({
  name: "App",
  components: {
    LogoutButton
  },
  data: () => ({
    appTopHeight: 0,
    isAuthenticated: false,
    drawer: true,
    navDrawer: true,
    appBar: true,
    date: new Date().toISOString().substr(0, 10),
    datePickerMenu: false,
    fileTypes: FILE_TYPES,
    fileTypesDict: FILE_TYPES_DICT,
    fileType: null as any,
    attachment: null as any,
    application: null as any,
    devices: [] as Array<any>,
    searchDevice: null as any,
    selectedDevice: null as any,
    reportId: null as any,
    isLoadingDevices: false,
    toggleFiles: false
  }),
  watch: {
    reportId(value: any) {
      if (value) {
        this.$router.push({
          name: "shipping-report-detail",
          params: { id: value }
        });
      }
    },
    date(value: any) {
      this.fileType = null;
    }
  },
  created() {
    this.appTopHeight = this.$vuetify.application.top;
    this.autoLogout();
  },
  methods: {
    test() {
      console.log(123);
    },
    onUploadFiles({ file, id }: any) {
      if (file) {
        // if cars is empty
        if (this.devices.length === 0) {
          this.getDevices();
        }
      }
    },
    onSetNavigationDrawerValue(value: boolean) {
      this.navDrawer = value;
    },
    onSetAppBarValue(value: boolean) {
      this.appBar = value;
    },
    async getDevices() {
      this.isLoadingDevices = true;
      let response = await DevicesRepository.get();
      while (response.data.next) {
        response = await DevicesRepository.get(
          response.data.next
            .split("?")
            .pop()
            .split("&")
            .filter((item: string) => ~item.indexOf("page="))[0]
            .split("=")
            .pop()
        );
        this.devices.push(...response.data.results);
      }
      this.isLoadingDevices = false;
    },
    async createReport() {
      const formData = new FormData();
      formData.append("date", this.date);
      formData.append("file_type", this.fileType);
      formData.append("attachment", this.attachment || "");
      formData.append("application", this.application || "");
      formData.append("device", this.selectedDevice);
      console.log(formData);
      const response = await ReportsRepository.createReport(formData);
      this.reportId = response.data.id;
    },
    async autoLogout() {
      Repository.interceptors.response.use(
        response => {
          return response;
        },
        error => {
          if (error.config && error.response && error.response.status === 401) {
            this.$store.dispatch(AUTH.LOGOUT, error);
            this.$router.push("/login");
          }
          return Promise.reject(error.response);
        }
      );
    }
  }
});
</script>

<style src="@/styles/main.scss" lang="scss"></style>

<style lang="scss" scoped>
.container-overflow {
  height: calc(100vh - var(--appTopHeight));
}
</style>
