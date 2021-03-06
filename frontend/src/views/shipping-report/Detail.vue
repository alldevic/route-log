<template lang='pug'>
  div.container-overflow
    v-expand-transition
      ecotec-map(
        v-show="itemActive"
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
      loading-text="Выполняется подгрузка фактов отгрузки..."
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

      template(v-slot:item.nav_mt_id="{ item }")
        span(v-if="item.nav_mt_id") {{ item.nav_mt_id }}
        span(v-else) Нет данных

      template(v-slot:item.datetime_entry="{ item }")
        span {{ item.datetime_entry | date }}

      template(v-slot:item.datetime_exit="{ item }")
        span {{ item.datetime_exit | date }}

      template(v-slot:item.action="{ item }")
        v-btn-toggle(borderless dense)
          v-btn(color="transparent" icon @click.stop="editItem(item)")
            v-icon(small) mdi-pencil
          v-btn(color="transparent" icon @click.stop="deleteItem(item)")
            v-icon(small) mdi-delete

      template(v-slot:top)
        v-toolbar(flat color="white")
          v-toolbar-title
            h4 Отчёт
          v-spacer
          .actions(v-if="!isLoadingContainerUnloads")
            v-btn.mr-2(color="light-green darken-1" dark @click="exportExcel")
              | Скачать
            v-dialog(v-model="dialogForDeleteItem" max-width="500px")
              v-card
                v-card-title
                  span.headline Удаление текущего вывоза
                v-card-text
                  p Вы уверены, что хотите удалить текущий вывоз (Код: {{ deletedItemId }})?
                  v-card-actions
                    v-spacer
                    v-btn(color="blue darken-1" text @click="closeDialogForDeleteItem")
                      | Отменить
                    v-btn(color="error" @click="deleteUnload")
                      | Удалить
            v-dialog(v-model="dialogForAddItem" max-width="500px" @click:outside="closeDialogForEditItem")
              template(v-slot:activator="{ on }")
                v-btn(color="primary" dark v-on="on")
                  | Добавить доп. вывоз
              v-card
                v-card-title
                  span.headline {{ formTitle }}

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
                                v-model="editedItem.date_entry"
                                clearable
                                label="Дата"
                                prepend-icon="event"
                                v-on="on"
                                required
                                :rules="dateEntryRules"
                              )
                            v-date-picker(
                              v-model="editedItem.date_entry"
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
                            :return-value.sync="editedItem.time_entry"
                            offset-y
                            max-width="290px"
                            min-width="290px"
                          )
                            template(v-slot:activator="{ on }")
                              v-text-field(
                                v-model="editedItem.time_entry"
                                clearable
                                label="Время"
                                prepend-icon="access_time"
                                readonly
                                v-on="on"
                                required
                                :rules="timeEntryRules"
                              )
                            v-time-picker(
                              v-model="editedItem.time_entry"
                              format="24hr"
                              color="primary"
                              @click:minute="$refs.menuForEntryTime.save(editedItem.time_entry)"
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
                                v-model="editedItem.date_exit"
                                clearable
                                label="Дата"
                                prepend-icon="event"
                                v-on="on"
                                required
                                :rules="dateExitRules"
                              )
                            v-date-picker(
                              v-model="editedItem.date_exit"
                              color="primary"
                              no-title
                              first-day-of-week=1
                              :min="editedItem.date_entry"
                              @input="datePickerExitMenu = false"
                            )
                          v-menu(
                            ref="menuForExitTime"
                            v-model="timePickerExitMenu"
                            transition="scroll-y-transition"
                            :close-on-content-click="false"
                            :return-value.sync="editedItem.time_exit"
                            offset-y
                            max-width="290px"
                            min-width="290px"
                          )
                            template(v-slot:activator="{ on }")
                              v-text-field(
                                v-model="editedItem.time_exit"
                                clearable
                                label="Время"
                                prepend-icon="access_time"
                                readonly
                                v-on="on"
                                required
                                :rules="timeExitRules"
                              )
                            v-time-picker(
                              v-model="editedItem.time_exit"
                              color="primary"
                              format="24hr"
                              :min="editedItem.time_entry"
                              @click:minute="$refs.menuForExitTime.save(editedItem.time_exit)"
                            )
                        v-col(cols="12")
                          v-autocomplete(
                            v-model="editedItem.geozone"
                            :items="geozones"
                            :loading="isLoadingGeozones"
                            :search-input.sync="searchGeozone"
                            auto-select-first
                            hide-selected
                            item-text="name"
                            item-value="id"
                            label="Площадки"
                            placeholder="Введите название площадки"
                            prepend-icon="mdi-database-search"
                            return-object
                          )
                          p(v-if="editedItem.nav_mt_obj") Найден код площадки из МТ: {{ editedItem.nav_mt_obj.mt_id }}
                            v-btn.ml-2(
                              small
                              :disabled="editedItem.nav_mt_id === editedItem.nav_mt_obj.mt_id"
                              depressed color="primary"
                              @click="setNavMtId"
                            ) Применить?
                        v-col(cols="12")
                          v-text-field(
                            v-model="editedItem.nav_mt_id"
                            label="Код площадки в МТ"
                            type="number"
                            required
                            :rules="navMtIdRules"
                          )
                        v-col(cols="12")
                          v-checkbox(v-model="editedItem.is_unloaded" color="primary" label="Отгружено")
                        v-col(cols="12")
                          v-text-field(
                            v-model="editedItem.value"
                            label="Объем контейнера"
                            type="number"
                            required
                            :rules="valueRules"
                          )
                        v-col(cols="12")
                          v-text-field(
                            v-model="editedItem.directory"
                            label="Муниципальное образование"
                            required
                            :rules="directoryRules"
                          )
                        v-col(cols="12")
                          v-text-field(
                            v-model="editedItem.container_type"
                            label="Тип контейнера"
                            required
                            :rules="containerTypeRules"
                          )
                        v-col(cols="12")
                          v-text-field(
                            v-model="editedItem.count"
                            label="Количество отгрузок"
                            type="number"
                            required
                            :rules="countRules"
                          )
                  v-card-actions
                    v-spacer
                    v-btn(color="blue darken-1" text @click="closeDialogForEditItem")
                      | Отменить
                    v-btn(color="primary" :disabled="!valid" @click="validate")
                      | {{ buttonText }}
          v-dialog(
            v-model="dialogUnloadsFilter"
            max-width="500px"
          )
            template(v-slot:activator="{ on }")
              v-badge(
                bordered
                color="error"
                dot
                overlap
                :value="unloadsFilterIsActive"
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
                span.headline Фильтр фактов отгрузки

              v-card-text
                v-container
                  v-form(ref="filter")
                    v-row
                      v-col(cols="12")
                        v-select(
                          v-model="unloadsFilter.is_unloaded"
                          :items="unloadStatuses"
                          item-text="name"
                          item-value="value"
                          label="Статус отгрузки"
                          clearable
                          hide-details
                        )
                      v-col(cols="12")
                        v-select(
                          v-model="unloadsFilter.container_type"
                          :items="containerTypes"
                          :loading="isLoadingContainerTypes"
                          item-text="text"
                          item-value="id"
                          label="Тип контейнера"
                          clearable
                          hide-details
                        )
                      v-col(cols="12")
                        v-text-field(
                          v-model="unloadsFilter.value"
                          label="Объем контейнера"
                          type="number"
                          clearable
                          hide-details
                        )
                      v-col(cols="12")
                        v-text-field(
                          v-model="unloadsFilter.directory__contains"
                          label="Муниципальное образование"
                          clearable
                          hide-details
                        )
                v-card-actions
                  v-spacer
                  v-btn(color="blue darken-1" text @click="dialogUnloadsFilter = false")
                    | Закрыть
                  v-btn(v-if="unloadsFilterIsActive" color="orange darken-1" dark @click="cleanFilter")
                    | Очистить
                  v-btn(color="primary" @click="acceptFilter")
                    | Применить
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
import _ from "lodash";
import EcotecMap from "@/components/EcotecMap.vue";
import RepositoryFactory from "@/api/RepositoryFactory";
import UNLOADS_STATUSES_DICT from "@/dictionaries/unloadsStatusesDict";

const ReportsRepository = RepositoryFactory.get("reports");
const GeozonesRepository = RepositoryFactory.get("geozones");
const ContainerTypesRepository = RepositoryFactory.get("containerTypes");

export default Vue.extend({
  components: {
    EcotecMap
  },
  filters: {
    date(date: any) {
      if (!date) return "Нет данных";

      return new Date(date).toLocaleString('ru', { hour12: false });
    }
  },
  data: () => ({
    mapZoom: 15,
    report: null as any,
    debouncedGeozones: null as any,
    valid: true,
    init: false,
    geozones: [] as Array<any>,
    searchGeozone: null as any,
    containerUnloads: [] as Array<any>,
    itemActive: false,
    isLoadingGeozones: false,
    isLoadingContainerTypes: false,
    isLoadingContainerUnloads: false,
    selectedContainerUnload: [] as Array<any>,
    page: 1,
    pageCount: 0,
    itemsPerPage: 30,
    isLoadingMtKey: false,
    deletedItemId: undefined as any,
    editedItemId: undefined as any,
    dialogForAddItem: false,
    dialogForDeleteItem: false,
    dialogUnloadsFilter: false,
    datePickerEntryMenu: false,
    datePickerExitMenu: false,
    timePickerEntryMenu: false,
    timePickerExitMenu: false,
    containerTypes: [] as Array<any>,
    unloadStatuses: UNLOADS_STATUSES_DICT,
    unloadsFilter: {
      is_unloaded: null as any,
      value: null as any,
      container_type: null as any,
      directory__contains: '' as string,
    },
    editedIndex: -1,
    editedItem: {
      date_entry: null as any,
      date_exit: null as any,
      time_entry: null as any,
      time_exit: null as any,
      datetime_entry: null as any,
      datetime_exit: null as any,
      geozone: {
        id: undefined as any,
        name: null as any
      },
      nav_mt_obj: null as any,
      is_unloaded: false as boolean,
      value: null as any,
      container_type: null as any,
      directory: null as any,
      count: null as any,
      nav_mt_id: null as any
    },
    defaultItem: {
      date_entry: null as any,
      date_exit: null as any,
      time_entry: null as any,
      time_exit: null as any,
      geozone: {
        id: undefined as any,
        name: null as any
      },
      nav_mt_obj: null as any,
      datetime_entry: null as any,
      datetime_exit: null as any,
      is_unloaded: false as boolean,
      value: null as any,
      container_type: null as any,
      directory: null as any,
      count: null as any,
      nav_mt_id: null as any
    },
    dateEntryRules: [(v: any) => !!v || "Дата не выбрана"],
    dateExitRules: [(v: any) => !!v || "Дата не выбрана"],
    timeEntryRules: [(v: any) => !!v || "Время не выбрано"],
    timeExitRules: [(v: any) => !!v || "Время не выбрано"],
    valueRules: [(v: any) => !!v || "Объем не указан"],
    containerTypeRules: [(v: any) => !!v || "Тип не указан"],
    directoryRules: [(v: any) => !!v || "Муниципальное образование не указано"],
    countRules: [(v: any) => !!v || "Количество не указано"],
    navMtIdRules: [(v: any) => !!v || "Код не указан"],
    headers: [
      {
        text: "Код площадки в МТ",
        value: "nav_mt_id",
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
      },
      {
        text: "Действия",
        value: "action",
        sortable: false
      }
    ]
  }),
  computed: {
    containerTypesIsEmpty() {
      return !this.containerTypes.length;
    },
    unloadsFilterIsActive() {
      const queries = this.$route.query;
      return queries.is_unloaded || queries.container_type || queries.value || queries.directory__contains
        ? true
        : !true;
    },
    currentItem() {
      const [currentItem] = this.selectedContainerUnload;
      return currentItem;
    },
    formTitle() {
      return this.editedIndex === -1
        ? "Добавить дополнительный вывоз"
        : "Редактировать текущий вывоз";
    },
    buttonText() {
      return this.editedIndex === -1 ? "Добавить" : "Редактировать";
    }
  },
  watch: {
    $route: {
      handler(route: any) {
        const reportId = Number(route.params.id);
        if ((route.query.page === undefined || route.query.page === '0') && route.params.id !== undefined) {
          this.$router.push({ path: `/shipping-report-detail/${route.params.id}?page=1` });
        } else {
          this.report = reportId;
          this.page = Number(route.query.page);
          this.unloadsFilter.is_unloaded =
            route.query.is_unloaded !== undefined
              ? route.query.is_unloaded
              : null;
          this.unloadsFilter.container_type =
            route.query.container_type !== undefined
              ? Number(route.query.container_type)
              : null;
          this.unloadsFilter.value =
            route.query.value !== undefined ? Number(route.query.value) : null;
          this.unloadsFilter.directory__contains =
            route.query.directory__contains !== undefined ? route.query.directory__contains : '';
          this.getContainerUnloads();
        }
      },
      immediate: true
    },
    selectedContainerUnload(itemNew: any, itemOld: any) {
      if (itemNew.length) {
        this.itemActive = true;
      } else {
        this.itemActive = false;
      }
    },
    editedItem: {
      handler(val: any) {
        if (val.geozone) {
          this.geozones = [val.geozone];

          if (val.geozone.id) {
            this.getMtKey(val.geozone.id);
          }
        }
      },
      deep: true
    },
    searchGeozone(val: string) {
      if (this.isLoadingGeozones) return;
      this.debouncedGeozones(val);
    },
    dialogUnloadsFilter(value: boolean) {
      if (value && this.containerTypesIsEmpty) {
        this.getContainerTypes();
      }
    },
  },
  created() {
    this.debouncedGeozones = _.debounce((name: string) => {
      this.getGeozonesByName(name);
    }, 300);
  },
  methods: {
    async getMtKey(id: number) {
      const response = await GeozonesRepository.getMtKey(id);
      const [firstNavMtObject] = response.data.results;
      this.editedItem.nav_mt_obj = firstNavMtObject;
    },
    async getGeozonesByName(name: string) {
      this.isLoadingGeozones = true;
      const response = await GeozonesRepository.getByName(
        name,
        this.editedItem.date_entry
      );
      this.geozones = response.data.results;
      this.isLoadingGeozones = false;
    },
    async addUnloadSet() {
      const reportId = this.report;
      const unloadSet = {
        report: reportId,
        datetime_entry: `${this.editedItem.date_entry} ${this.editedItem.time_entry}`,
        datetime_exit: `${this.editedItem.date_exit} ${this.editedItem.time_exit}`,
        is_unloaded: this.editedItem.is_unloaded,
        value: this.editedItem.value,
        container_type: this.editedItem.container_type,
        directory: this.editedItem.directory,
        count: this.editedItem.count
      };
      const response = await ReportsRepository.addUnloadsSet(unloadSet);
      this.getContainerUnloads();
    },
    async getContainerUnloads() {
      this.isLoadingContainerUnloads = true;
      const id = this.report;
      const pageNumber = this.page;
      const filterData = this.unloadsFilter;
      const response = await ReportsRepository.getContainerUnloads(
        id,
        pageNumber,
        filterData
      );
      this.containerUnloads = response.data.results;
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
    editItem(item: any) {
      this.editedItemId = item.id;
      this.editedIndex = this.containerUnloads.indexOf(item);
      let dateEntry = null;
      let timeEntry = null;
      let dateExit = null;
      let timeExit = null;

      if (item.datetime_entry) {
        const dateTimeEntry = new Date(item.datetime_entry);
        const reversedDateArray = dateTimeEntry
          .toLocaleDateString()
          .split(".")
          .reverse();
        dateEntry = reversedDateArray.join("-");
        timeEntry = dateTimeEntry.toLocaleTimeString();
      }
      if (item.datetime_exit) {
        const dateTimeExit = new Date(item.datetime_exit);
        const reversedDateArray = dateTimeExit
          .toLocaleDateString()
          .split(".")
          .reverse();
        dateExit = reversedDateArray.join("-");
        timeExit = dateTimeExit.toLocaleTimeString();
      }
      this.editedItem = Object.assign(
        {},
        item,
        { date_entry: dateEntry },
        { time_entry: timeEntry },
        { date_exit: dateExit },
        { time_exit: timeExit }
      );
      this.dialogForAddItem = true;
    },
    deleteItem(item: any) {
      this.dialogForDeleteItem = true;
      this.deletedItemId = item.id;
    },
    setNavMtId() {
      const id = this.editedItem.nav_mt_obj.mt_id;
      this.editedItem.nav_mt_id = id;
    },
    async deleteUnload() {
      const id = this.deletedItemId;
      const response = await ReportsRepository.deleteUnload(id);
      this.getContainerUnloads();
      this.closeDialogForDeleteItem();
    },
    async saveUnloadChanges() {
      const id = this.editedItemId;
      const reportId = this.report;
      const unloadSet = {
        report: reportId,
        datetime_entry: `${this.editedItem.date_entry} ${this.editedItem.time_entry}`,
        datetime_exit: `${this.editedItem.date_exit} ${this.editedItem.time_exit}`,
        is_unloaded: this.editedItem.is_unloaded,
        value: this.editedItem.value,
        container_type: this.editedItem.container_type,
        directory: this.editedItem.directory,
        count: this.editedItem.count,
        nav_mt_id: this.editedItem.nav_mt_id
      };
      const response = await ReportsRepository.saveUnloadChanges(id, unloadSet);
      this.closeDialogForEditItem();
      this.getContainerUnloads();
    },
    closeDialogForEditItem() {
      this.editedItemId = undefined;
      this.dialogForAddItem = false;
      this.editedItem = Object.assign({}, this.defaultItem);
      this.editedIndex = -1;
    },
    closeDialogForDeleteItem() {
      this.deletedItemId = undefined;
      this.dialogForDeleteItem = false;
    },
    validate() {
      const vForm: any = this.$refs.form;
      if (vForm.validate()) {
        const func =
          this.editedIndex !== -1
            ? this.saveUnloadChanges()
            : this.addUnloadSet();
        this.dialogForAddItem = false;
        vForm.reset();
      }
    },
    updatePage(pageNumber: any) {
      this.page = pageNumber;
      let queries = Object.assign({}, { page: pageNumber });

      if (this.unloadsFilter.is_unloaded !== null) {
        queries = Object.assign(queries, {
          is_unloaded: this.unloadsFilter.is_unloaded
        });
      }
      if (this.unloadsFilter.container_type !== null) {
        queries = Object.assign(queries, {
          container_type: this.unloadsFilter.container_type
        });
      }
      if (this.unloadsFilter.value !== null) {
        queries = Object.assign(queries, { value: this.unloadsFilter.value });
      }
      if (this.unloadsFilter.directory__contains !== '') {
        queries = Object.assign(queries, { directory__contains: this.unloadsFilter.directory__contains });
      }

      this.$router.replace({
        name: 'shipping-report-detail',
        params: { id: this.report },
        query: queries,
      }).catch((error) => {});
    },
    async exportExcel() {
      const response = await ReportsRepository.exportReport(this.report);
      const fileURL = window.URL.createObjectURL(response.data);
      const fileLink = document.createElement("a");
      fileLink.href = fileURL;
      const filename = response.headers["content-disposition"].split(
        "filename="
      )[1];
      fileLink.setAttribute("download", filename);
      fileLink.setAttribute("target", "_blank");
      document.body.appendChild(fileLink);
      fileLink.click();
    },
    async getContainerTypes() {
      if (this.containerTypesIsEmpty) {
        this.isLoadingContainerTypes = true;
        let response = await ContainerTypesRepository.get();
        const responseTypes = response.data.results;
        while (response.data.next) {
          response = await ContainerTypesRepository.get(
            response.data.next
              .split("?")
              .pop()
              .split("&")
              .filter((item: string) => ~item.indexOf("page="))[0]
              .split("=")
              .pop()
          );
          responseTypes.push(...response.data.results);
        }
        this.containerTypes = responseTypes;
        this.isLoadingContainerTypes = false;
      }
    },
    acceptFilter() {
      this.updatePage(1);
      this.dialogUnloadsFilter = false;
    },
    cleanFilter() {
      const vForm: any = this.$refs.filter;
      vForm.reset();
      this.updatePage(1);
      this.dialogUnloadsFilter = false;
    }
    // parseDate(date: any) {
    //   if (!date) return null;

    //   const [year, month, day] = date.split('.');
    //   return `${year}-${month}-${day}`;
    // },
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
