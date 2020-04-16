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
                first-day-of-week=1
                @input="datePickerMenu = false"
              )
        v-divider(v-if="date")
        v-list-item
          v-list-item-content
            v-file-input(
              v-model="attachment"
              show-size
              counter
              accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
              :label="fileTypesDict[fileTypes.attachment].label"
              @change.sync="onUploadFiles({ file: $event, id: 1 })"
            )
        v-list-item
          v-list-item-content
            v-file-input(
              v-model="application"
              show-size
              counter
              accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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
        v-list-item(v-if="application || attachment")
          v-list-item-content
            v-combobox(
              v-model="selectedContainerTypes"
              :items="containerTypes"
              :search-input.sync="searchContainerType"
              item-text="text"
              item-value="id"
              hide-no-data
              clearable
              label="Выберите типы контейнеров"
              prepend-icon="flag"
              multiple
              small-chips
              deletable-chips
            )
        v-list-item
          v-list-item-content
            v-btn(
              @click="createReport"
              color="primary"
              depressed
              :loading="reportIsCreated"
              :disabled="!selectedDevice"
            ) Сформировать отчет
    v-app-bar(
      v-if="appBar"
      app dark flat
      color="blue-grey darken-3"
    )
      v-app-bar-nav-icon(@click.stop="drawer = !drawer")
      v-btn.mx-2(
        v-if="routeIsReportList"
        @click="routeToReportList"
        small depressed
        color="blue-grey darken-3"
      )
        v-icon.mr-1 arrow_back
        | Назад
      v-spacer
      logout-button

    v-content(:style="{ '--appTopHeight': appTopHeight }")
      router-view(
        @setAppBarValue="onSetAppBarValue"
        @setNavigationDrawerValue="onSetNavigationDrawerValue"
      )

      v-overlay(absolute :value="reportIsCreated")
        v-progress-circular(indeterminate size="64")
</template>

<script lang="ts">
import Vue from 'vue';
import LogoutButton from '@/components/LogoutButton.vue';
import Repository from '@/api/Repository';
import RepositoryFactory from '@/api/RepositoryFactory';
import FILE_TYPES from '@/constants/fileTypes';
import FILE_TYPES_DICT from '@/dictionaries/fileTypesDict';
import AUTH from './store/actions/auth';

const DevicesRepository = RepositoryFactory.get('devices');
const ContainerTypesRepository = RepositoryFactory.get('containerTypes');
const ReportsRepository = RepositoryFactory.get('reports');

export default Vue.extend({
  name: 'App',
  components: {
    LogoutButton,
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
    containerTypes: [] as Array<any>,
    searchDevice: null as any,
    searchContainerType: null as any,
    selectedDevice: null as any,
    selectedContainerTypes: [] as Array<any>,
    reportId: null as any,
    isLoadingDevices: false,
    isLoadingContainerTypes: false,
    toggleFiles: false,
    reportIsCreated: false,
  }),
  computed: {
    routeIsReportList() {
      return this.$route.name === 'shipping-report-detail';
    },
  },
  watch: {
    reportId(value: any) {
      if (value) {
        this.$router.push({
          name: 'shipping-report-detail',
          params: { id: value },
          query: { page: '1' },
        });
      }
    },
    date(value: any) {
      this.fileType = null;
    },
    application(value: any) {
      if (!value) {
        this.selectedDevice = null;
      }
    },
    attachment(value: any) {
      if (!value) {
        this.selectedDevice = null;
      }
    },
  },
  created() {
    this.appTopHeight = this.$vuetify.application.top;
    this.autoLogout();
  },
  methods: {
    test() {
      // console.log(123);
    },
    routeToReportList() {
      this.$router.push({ name: 'shipping-report-list', query: { page: '1' } });
    },
    onUploadFiles({ file, id }: any) {
      if (file) {
        // if cars is empty
        if (this.devices.length === 0) {
          this.getDevices();
        }
        if (this.containerTypes.length === 0) {
          this.getContainerTypes();
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
      let response = await DevicesRepository.get({ date: this.date });
      const responseDevices = response.data.results;
      while (response.data.next) {
        response = await DevicesRepository.get({
          page: response.data.next
            .split("?")
            .pop()
            .split("&")
            .filter((item: string) => ~item.indexOf("page="))[0]
            .split("=")
            .pop(),
          date: this.date
        });
        responseDevices.push(...response.data.results);
      }
      this.devices = responseDevices;
      this.isLoadingDevices = false;
    },
    async getContainerTypes() {
      this.isLoadingContainerTypes = true;
      let response = await ContainerTypesRepository.get();
      const responseTypes = response.data.results;
      while (response.data.next) {
        response = await ContainerTypesRepository.get(
          response.data.next
            .split('?')
            .pop()
            .split('&')
            .filter((item: string) => ~item.indexOf('page='))[0]
            .split('=')
            .pop(),
        );
        responseTypes.push(...response.data.results);
      }
      this.containerTypes = responseTypes;
      this.isLoadingContainerTypes = false;
    },
    async createReport() {
      this.reportIsCreated = true;
      const formData = new FormData();
      formData.append('date', this.date);
      formData.append('file_type', this.fileType);
      formData.append('attachment', this.attachment || '');
      formData.append('application', this.application || '');
      formData.append('device', this.selectedDevice);
      this.selectedContainerTypes.map((x: any) => formData.append('container_types', x.id));
      // console.log(formData);
      const response = await ReportsRepository.createReport(formData);
      this.selectedDevice = null;
      this.reportId = response.data.id;
      this.reportIsCreated = false;
    },
    async autoLogout() {
      Repository.interceptors.response.use(
        response => response,
        (error) => {
          if (error.config && error.response && error.response.status === 401) {
            this.$store.dispatch(AUTH.LOGOUT, error);
            this.$router.push('/login');
          }
          return Promise.reject(error.response);
        },
      );
    },
  },
});
</script>

<style src="@/styles/main.scss" lang="scss"></style>

<style lang="scss" scoped>
.container-overflow {
  height: calc(100vh - var(--appTopHeight));
}
</style>
