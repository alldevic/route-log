<template lang='pug'>
  v-container.container-overflow(class="pa-0")
    v-data-table.section-overflow(
      :headers="headers"
      :items="reports"
      :loading="isLoadingReports"
      :server-items-length="pageCount"
      :page.sync="page"
      item-key="id"
      fixed-header
      @click:row="toDetailPage"
      @update:page="updatePage"
      loading-text="Выполняется подгрузка отчётов..."
      :footer-props="{\
        'disable-items-per-page': true,\
        'items-per-page-options': [itemsPerPage],\
        'disable-pagination': isLoadingReports,\
      }"
    )
      template(v-slot:item.device="{ item }")
        span(v-if="(item.device)")
          span(v-if="(item.device.name && item.device.reg_number)") {{item.device.name}} / {{item.device.reg_number}}
          span(v-else-if="(item.device.reg_number)") {{item.device.reg_number}}
          span(v-else-if="(item.device.name)") {{item.device.name}}
        span(v-else) Нет данных
      template(v-slot:top)
        v-toolbar(flat color="white")
          v-toolbar-title
            h4 Список отчётов
          v-spacer
          .actions(v-if="!isLoadingReports")
            v-dialog(
              v-model="dialogReportsFilter"
              max-width="500px"
            )
              template(v-slot:activator="{ on }")
                v-badge(
                  bordered
                  color="error"
                  dot
                  overlap
                  :value="reportsFilterIsActive"
                )
                  v-btn(
                    v-on="on"
                    color="primary"
                    fab
                    x-small
                  ).ml-2
                    v-icon filter_list

              v-card
                v-card-title
                  span.headline Фильтр списка отчётов

                v-card-text
                  v-container
                    v-form(ref="filter")
                      v-row
                        v-col(cols="12")
                          v-text-field(
                            v-model="reportsFilter.id"
                            label="Код отчёта"
                            type="number"
                            clearable
                            disabled
                            hide-details
                          )
                        v-col(cols="12")
                          v-menu(
                            v-model="reportDateMenu"
                            :close-on-content-click="false"
                            :nudge-right="40"
                            transition="scale-transition"
                            offset-y
                            min-width="290px"
                          )
                            template(v-slot:activator="{ on }")
                              v-text-field(
                                v-model="reportsFilter.date"
                                label="Дата"
                                clearable
                                prepend-icon="event"
                                hide-details
                                readonly
                                v-on="on"
                              )
                            v-date-picker(
                              v-model="reportsFilter.date"
                              @input="reportDateMenu = false"
                            )
                        v-col(cols="12")
                          v-autocomplete(
                            v-model="reportsFilter.device"
                            :items="devices"
                            :search-input.sync="searchDevice"
                            :loading="isLoadingDevices"
                            item-text="name"
                            item-value="id"
                            hide-no-data
                            clearable
                            label="Автомобиль"
                            prepend-icon="directions_car"
                          )
                  v-card-actions
                    v-spacer
                    v-btn(color="blue darken-1" text @click="dialogReportsFilter = false")
                      | Закрыть
                    v-btn(v-if="reportsFilterIsActive" color="orange darken-1" dark @click="cleanFilter")
                      | Очистить
                    v-btn(color="primary" @click="acceptFilter")
                      | Применить
</template>

<script lang="ts">
import Vue from "vue";
import RepositoryFactory from "@/api/RepositoryFactory";

const ReportsRepository = RepositoryFactory.get("reports");
const DevicesRepository = RepositoryFactory.get("devices");

export default Vue.extend({
  data: () => ({
    reports: [] as Array<any>,
    isLoadingReports: false,
    pageCount: 0,
    itemsPerPage: 30,
    page: 1,
    devices: [] as Array<any>,
    isLoadingDevices: false,
    searchDevice: null as any,
    reportDateMenu: false,
    reportsFilter: {
      id: undefined as any,
      date: undefined as any,
      device: undefined as any
    },
    dialogReportsFilter: false,
    headers: [
      {
        text: "Код отчёта",
        value: "id",
        sortable: false
      },
      {
        text: "Дата",
        value: "date",
        sortable: false
      },
      {
        text: "Автомобиль",
        value: "device",
        sortable: false
      }
    ]
  }),
  computed: {
    reportsIsNotEmpty() {
      return this.reports.length;
    },
    devicesIsEmpty() {
      return !this.devices.length;
    },
    reportsFilterIsActive() {
      const queries = this.$route.query;
      return queries.id || queries.date || queries.device ? true : !true;
    }
  },
  watch: {
    $route: {
      handler(route: any) {
        if (route.query.page && route.query.page !== "0") {
          this.page = Number(route.query.page);
          // this.reportsFilter.id = route.query.id !== undefined ? Number(route.query.id) : undefined;
          this.reportsFilter.date =
            route.query.date !== undefined ? route.query.date : undefined;
          this.reportsFilter.device =
            route.query.device !== undefined
              ? Number(route.query.device)
              : undefined;
          this.getReports();
        } else {
          this.$router.push({ path: "/shipping-report-list/?page=1" });
        }
      },
      immediate: true
    },
    reports(value: any) {
      if (!value) {
        value = [];
      }
    },
    dialogReportsFilter(value: boolean) {
      if (value && this.devicesIsEmpty) {
        this.getDevices();
      }
    }
  },
  methods: {
    async getReports() {
      this.isLoadingReports = true;
      const pageNumber = this.page;
      const filterData = this.reportsFilter;
      const response = await ReportsRepository.get(pageNumber, filterData);
      this.reports = response.data.results;
      this.pageCount = response.data.count;
      this.isLoadingReports = false;
    },
    async getDevices() {
      this.isLoadingDevices = true;
      let response = await DevicesRepository.get({ page: 1 });
      const responseDevices = response.data.results;
      while (response.data.next) {
        response = await DevicesRepository.get({
          page: response.data.next
            .split("?")
            .pop()
            .split("&")
            .filter((item: string) => ~item.indexOf("page="))[0]
            .split("=")
            .pop()
        });
        responseDevices.push(...response.data.results);
      }
      this.devices = responseDevices;
      this.isLoadingDevices = false;
    },
    updatePage(pageNumber: any) {
      this.page = pageNumber;
      let queries = Object.assign({}, { page: pageNumber });

      // if (this.reportsFilter.id !== undefined) {
      //   queries = Object.assign(queries, { id: this.reportsFilter.id });
      // }
      if (this.reportsFilter.date !== undefined) {
        queries = Object.assign(queries, { date: this.reportsFilter.date });
      }
      if (this.reportsFilter.device !== undefined) {
        queries = Object.assign(queries, { device: this.reportsFilter.device });
      }
      this.$router
        .replace({
          name: "shipping-report-list",
          query: queries
        })
        .catch(error => {});
    },
    toDetailPage(report: any) {
      this.$router.push({
        name: "shipping-report-detail",
        params: { id: report.id },
        query: { page: "1" }
      });
    },
    acceptFilter() {
      this.updatePage(1);
      this.dialogReportsFilter = false;
    },
    cleanFilter() {
      const vForm: any = this.$refs.filter;
      vForm.reset();
      this.updatePage(1);
      this.dialogReportsFilter = false;
    }
  }
});
</script>
