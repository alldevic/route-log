import Repository from '../Repository';

const resource = 'reports/';

export default {
  createReport(option: any) {
    // const config = { headers: { 'Content-Type': 'multipart/form-data' } };
    return Repository.post(`${resource}make-report/`, option);
  },
  addUnloadsSet(option: any) {
    return Repository.post(`${resource}unloads-set/`, option);
  },
  deleteUnload(id: number) {
    return Repository.delete(`${resource}unloads-set/${id}/`);
  },
  saveUnloadChanges(id: number, option: any) {
    return Repository.put(`${resource}unloads-set/${id}/`, option);
  },
  getReport(id: number) {
    return Repository.get(`${resource}${id}/`);
  },
  getContainerUnloads(id: number, page: number, filterData: any) {
    const is_unloaded = filterData.is_unloaded !== null ? `&is_unloaded=${filterData.is_unloaded}` : '';
    const container_type = filterData.container_type !== null ? `&container_type=${filterData.container_type}` : '';
    const value = filterData.value !== null ? `&value=${filterData.value}` : '';

    return Repository.get(`${resource}unloads-set/?report=${id}&page=${page || 1}${is_unloaded}${container_type}${value}`);
  },
  get(page: number, filterData: any) {
    // const id = filterData.id !== undefined ? `&id=${filterData.id}` : '';
    const date = filterData.date !== undefined ? `&date=${filterData.date}` : '';
    const device = filterData.device !== undefined ? `&device=${filterData.device}` : '';

    return Repository.get(`${resource}reports-set/?page=${page || 1}${date}${device}`);
  },
  exportReport(id: number) {
    return Repository.get(`${resource}export-report/${id}/`, {
      responseType: 'blob',
      timeout: 30000,
    });
  },
};
