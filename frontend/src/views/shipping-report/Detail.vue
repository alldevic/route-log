<template lang='pug'>
  div.container-overflow
    v-expand-transition
      ecotec-map(
        :item="currentItem"
        :map-height="380"
      )
    v-data-table.section-overflow(
      v-model="selectedContainerUnload"
      :headers="headers"
      :items="containerUnloads"
      :loading="isLoadingContainerUnloads"
      :server-items-length="pageCount"
      :page.sync="page"
      item-key="id"
      fixed-header
      single-select
      @click:row="getRowValue"
      @update:page="updatePage"
      loading-text="Выполняется подгрузка отчётов..."
      :footer-props="{\
        'disable-items-per-page': true,\
        'items-per-page-options': [itemsPerPage],\
        'disable-pagination': isLoadingContainerUnloads,\
      }"
    )
      template(v-slot:item.is_unloaded="{ item }")
        span(v-if="item.is_unloaded === true") Да
        span(v-if="item.is_unloaded === false") Нет
        span(v-if="item.is_unloaded === undefined")
          | Информация отсутствует
          
      template(v-slot:item.datetime_entry="{ item }")
        span {{ item.datetime_entry | date }}

      template(v-slot:item.datetime_exit="{ item }")
        span {{ item.datetime_exit | date }}

      template(v-slot:top)
        v-toolbar(flat color="white")
          v-toolbar-title
            h4 Отчёт
          v-spacer
          v-btn.mr-2(color="light-green darken-1" dark @click="exportExcel")
            | Скачать
          v-dialog(v-model="dialogForAddItem" max-width="500px")
            template(v-slot:activator="{ on }")
              v-btn(color="primary" dark v-on="on")
                | Добавить доп. вывоз
            v-card
              v-card-title
                span.headline Добавить дополнительный вывоз

              v-card-text
                v-container
                  v-form(ref="form" v-model="valid" lazy-validation)
                    v-row
                      v-col(cols="12")
                        p.caption Дата и время въезда
                        v-menu(
                          v-model="datePickerEntryMenu"
                          transition="scroll-y-transition"
                          offset-y
                          max-width="290px"
                          min-width="290px"
                        )
                          template(v-slot:activator="{ on }")
                            v-text-field(
                              v-model="dateEntry"
                              clearable
                              label="Дата"
                              prepend-icon="event"
                              v-on="on"
                              required
                              :rules="dateEntryRules"
                            )
                          v-date-picker(
                            v-model="dateEntry"
                            color="primary"
                            no-title
                            first-day-of-week=1
                            @input="datePickerEntryMenu = false"
                          )
                        v-menu(
                          ref="menuForEntryTime"
                          v-model="timePickerEntryMenu"
                          transition="scroll-y-transition"
                          :close-on-content-click="false"
                          :return-value.sync="timeEntry"
                          offset-y
                          max-width="290px"
                          min-width="290px"
                        )
                          template(v-slot:activator="{ on }")
                            v-text-field(
                              v-model="timeEntry"
                              clearable
                              label="Время"
                              prepend-icon="access_time"
                              readonly
                              v-on="on"
                              required
                              :rules="timeEntryRules"
                            )
                          v-time-picker(
                            v-model="timeEntry"
                            color="primary"
                            @click:minute="$refs.menuForEntryTime.save(timeEntry)"
                          )
                      v-col(cols="12")
                        p.caption Дата и время выезда
                        v-menu(
                          v-model="datePickerExitMenu"
                          transition="scroll-y-transition"
                          offset-y
                          max-width="290px"
                          min-width="290px"
                        )
                          template(v-slot:activator="{ on }")
                            v-text-field(
                              v-model="dateExit"
                              clearable
                              label="Дата"
                              prepend-icon="event"
                              v-on="on"
                              required
                              :rules="dateExitRules"
                            )
                          v-date-picker(
                            v-model="dateExit"
                            color="primary"
                            no-title
                            first-day-of-week=1
                            @input="datePickerExitMenu = false"
                          )
                        v-menu(
                          ref="menuForExitTime"
                          v-model="timePickerExitMenu"
                          transition="scroll-y-transition"
                          :close-on-content-click="false"
                          :return-value.sync="timeExit"
                          offset-y
                          max-width="290px"
                          min-width="290px"
                        )
                          template(v-slot:activator="{ on }")
                            v-text-field(
                              v-model="timeExit"
                              clearable
                              label="Время"
                              prepend-icon="access_time"
                              readonly
                              v-on="on"
                              required
                              :rules="timeExitRules"
                            )
                          v-time-picker(
                            v-model="timeExit"
                            color="primary"
                            @click:minute="$refs.menuForExitTime.save(timeExit)"
                          )
                      v-col(cols="12")
                        v-checkbox(v-model="isUnloaded" color="primary" label="Отгружено")
                      v-col(cols="12")
                        v-text-field(
                          v-model="value"
                          label="Объем контейнера"
                          type="number"
                          required
                          :rules="valueRules"
                        )
                      v-col(cols="12")
                        v-text-field(
                          v-model="containerType"
                          label="Тип контейнера"
                          required
                          :rules="containerTypeRules"
                        )
                      v-col(cols="12")
                        v-text-field(
                          v-model="directory"
                          label="Муниципальное образование"
                          required
                          :rules="directoryRules"
                        )
                      v-col(cols="12")
                        v-text-field(
                          v-model="count"
                          label="Количество отгрузок"
                          type="number"
                          required
                          :rules="countRules"
                        )
                v-card-actions
                  v-spacer
                  v-btn(color="blue darken-1" text @click="close")
                    | Отменить
                  v-btn(color="primary" :disabled="!valid" @click="validate")
                    | Добавить
      //- template(v-slot:body="{ items, expand, isExpanded }")
      //-   tbody
      //-     tr(v-for="item in items" :key="item.name" @click="expand(!isExpanded)")
      //-       td(v-if="!isExpanded") {{ item.id }}
      //-       td {{ item.datetime_entry | date }}
      //-       td {{ item.datetime_exit | date }}
      //-       td {{ item.is_unloaded }}
      //-       td {{ item.value }}
      //-       td {{ item.container_type }}
      //-       td {{ item.directory }}
      //-       td {{ item.count }}
</template>

<script lang="ts">
import Vue from "vue";
import EcotecMap from "@/components/EcotecMap.vue";
import RepositoryFactory from "@/api/RepositoryFactory";

const ReportsRepository = RepositoryFactory.get("reports");

export default Vue.extend({
  components: {
    EcotecMap
  },
  data: () => ({
    mapZoom: 15,
    report: null as any,
    valid: true,
    init: false,
    containerUnloads: [] as Array<any>,
    itemActive: false,
    isLoadingContainerUnloads: false,
    selectedContainerUnload: [] as Array<any>,
    page: 1,
    pageCount: 1,
    itemsPerPage: 30,
    dialogForAddItem: false,
    datePickerEntryMenu: false,
    datePickerExitMenu: false,
    timePickerEntryMenu: false,
    timePickerExitMenu: false,
    dateEntry: null as any,
    dateExit: null as any,
    timeEntry: null as any,
    timeExit: null as any,
    isUnloaded: false as boolean,
    value: null as any,
    containerType: null as any,
    directory: null as any,
    count: null as any,
    dateEntryRules: [(v: any) => !!v || "Дата не выбрана"],
    dateExitRules: [(v: any) => !!v || "Дата не выбрана"],
    timeEntryRules: [(v: any) => !!v || "Время не выбрано"],
    timeExitRules: [(v: any) => !!v || "Время не выбрано"],
    valueRules: [(v: any) => !!v || "Объем не указан"],
    containerTypeRules: [(v: any) => !!v || "Тип не указан"],
    directoryRules: [(v: any) => !!v || "Муниципальное образование не указано"],
    countRules: [(v: any) => !!v || "Количество не указано"],
    headers: [
      {
        text: "Код",
        value: "id",
        sortable: false
      },
      {
        text: "Время въезда",
        value: "datetime_entry",
        sortable: false
      },
      {
        text: "Время выезда",
        value: "datetime_exit",
        sortable: false
      },
      {
        text: "Отгружено",
        value: "is_unloaded",
        sortable: false
      },
      {
        text: "Объем контейнера",
        value: "value",
        sortable: false
      },
      {
        text: "Тип контейнера",
        value: "container_type",
        sortable: false
      },
      {
        text: "Муниципальное образование",
        value: "directory",
        sortable: false
      },
      {
        text: "Количество отгрузок",
        value: "count",
        sortable: false
      }
    ]
  }),
  computed: {
    currentItem() {
      const [currentItem] = this.selectedContainerUnload;
      return currentItem;
    }
  },
  watch: {
    $route: {
      handler(route: any) {
        this.report = Number(route.params.id);
        this.page = Number(route.query.page);
        this.getContainerUnloads();
        this.activateBackButton();
      },
      immediate: true
    },
    selectedContainerUnload(itemNew: any, itemOld: any) {
      if (itemNew.length) {
        this.itemActive = true;
      } else {
        this.itemActive = false;
      }
    }
  },
  methods: {
    async addUnloadSet() {
      const reportId = this.report;
      const fullDateEntry = `${this.dateEntry} ${this.timeEntry}`;
      const fullDateExit = `${this.dateExit} ${this.timeExit}`;
      const unloadSet = {
        report: reportId,
        datetime_entry: fullDateEntry,
        datetime_exit: fullDateExit,
        is_unloaded: this.isUnloaded,
        value: this.value,
        container_type: this.containerType,
        directory: this.directory,
        count: this.count
      };
      const response = await ReportsRepository.addUnloadsSet(unloadSet);
      this.getContainerUnloads();
    },
    async getContainerUnloads() {
      this.isLoadingContainerUnloads = true;
      const id = this.report;
      const pageNumber = this.page;
      const response = await ReportsRepository.getContainerUnloads(
        id,
        pageNumber
      );
      this.containerUnloads = response.data.results;
      // console.log(this.containerUnloads);
      this.pageCount = response.data.count;
      this.isLoadingContainerUnloads = false;
    },
    getRowValue(item: any): void {
      if (item.geozone) {
        this.selectedContainerUnload = this.selectedContainerUnload.includes(
          item
        )
          ? []
          : [item];
        this.itemActive = !!this.selectedContainerUnload.length;
      }
    },
    close() {
      this.dialogForAddItem = false;
    },
    validate() {
      const vForm: any = this.$refs.form;
      if (vForm.validate()) {
        this.addUnloadSet();
        this.dialogForAddItem = false;
        vForm.reset();
      }
    },
    updatePage(pageNumber: any) {
      this.page = pageNumber;
      this.$router.push({
        name: "shipping-report-detail",
        params: { id: this.report },
        query: { page: pageNumber }
      });
    },
    activateBackButton() {
      const backButton = true;
      this.$emit("activateBackButton", backButton);
    },
    async exportExcel() {
      const response = await ReportsRepository.exportReport(this.report);
      var fileURL = window.URL.createObjectURL(response.data);
      var fileLink = document.createElement("a");
      fileLink.href = fileURL;
      const filename = response.headers["content-disposition"].split(
        "filename="
      )[1];
      fileLink.setAttribute("download", filename);
      fileLink.setAttribute("target", "_blank");
      document.body.appendChild(fileLink);
      fileLink.click();
    }
    // updatePage(pageNumber: any) {
    //   this.$router.push({
    //     name: 'shipping-report-detail',
    //     params: { id: this.report },
    //     query: { page: pageNumber },
    //   });
    // },
  }
});
</script>
