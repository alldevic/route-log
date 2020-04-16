<template lang='pug'>
  v-container.container-overflow(class="pa-0")
    v-card.section-overflow(
      flat tile
      height="100%" width="100%"
    )
      v-card-title.py-4
        h4 Список отчётов отгрузок
      v-card-text.pa-0.section-overflow
        template(v-if="reportsIsNotEmpty")
          v-list.content-overflow(subheader)
            v-list-item(
              v-for="report in reports"
              :key="report.id"
              :to="{ name: 'shipping-report-detail', params: { id: report.id }, query: { page: 1 } }"
              two-line
            )
              v-list-item-content
                v-list-item-title
                  h3 {{ report.id }}
                v-list-item-subtitle
                  p {{ report.date }}

          v-card-text.pa-0
            v-pagination.my-4(
              v-model="page"
              :length="reportsLength"
              :total-visible="7"
            )

        template(v-if="!reportsIsNotEmpty && !isLoadingReports")
          h4.px-4 {{ message }}

    v-overlay(absolute :value="isLoadingReports")
      v-progress-circular(indeterminate size="64")
</template>

<script lang="ts">
import Vue from 'vue';
import RepositoryFactory from '@/api/RepositoryFactory';

const ReportsRepository = RepositoryFactory.get('reports');

export default Vue.extend({
  data: () => ({
    reports: [] as Array<any>,
    isLoadingReports: false,
    reportsLength: 0,
    itemsPerPage: 30,
    page: 1,
    message: 'Список отчётов пуст!',
  }),
  computed: {
    reportsIsNotEmpty() {
      return this.reports.length;
    },
  },
  watch: {
    $route: {
      handler(route: any) {
        if (route.query.page) {
          this.page = Number(route.query.page);
          this.getReports();
          this.activateBackButton();
        }
      },
      immediate: true,
    },
    reports(value: any) {
      if (!value) {
        value = [];
      }
    },
    page: {
      handler(valueNew: any, valueOld: any) {
        if (valueNew !== valueOld) {
          this.$router
            .replace({
              name: 'shipping-report-list',
              query: { page: valueNew },
            })
            .catch((error) => {});
        }
      },
      immediate: true,
    },
  },
  methods: {
    async getReports() {
      this.isLoadingReports = true;
      const response = await ReportsRepository.get(this.page);
      this.reports = response.data.results;
      this.reportsLength = Math.ceil(response.data.count / this.itemsPerPage);
      this.isLoadingReports = false;
    },
    activateBackButton() {
      const backButton = false;
      this.$emit('activateBackButton', backButton);
    },
  },
});
</script>
