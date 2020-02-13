<template lang='pug'>
  v-container(class="pa-0")
    v-card.section-overflow(flat tile color="blue-grey lighten-5")
      v-card-title.pa-4
        h4 Список отчётов отгрузок
      v-card-text.section-overflow
        v-list(v-if="reports" subheader)
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
</template>

<script lang="ts">
import Vue from "vue";
import RepositoryFactory from "@/api/RepositoryFactory";

const ReportsRepository = RepositoryFactory.get("reports");

export default Vue.extend({
  data: () => ({
    reports: [] as Array<any>,
    isLoadingReports: false
  }),
  watch: {
    $route: {
      handler() {
        this.getReports();
      },
      immediate: true
    }
  },
  methods: {
    async getReports() {
      this.isLoadingReports = true;
      const response = await ReportsRepository.get();
      this.reports = response.data.results;
      this.isLoadingReports = false;
    }
  }
});
</script>
