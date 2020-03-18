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
  getContainerUnloads(id: number, page: number) {
    return Repository.get(`${resource}unloads-set/?report=${id}&page=${page || 1}`);
  },
  get(page: number) {
    return Repository.get(`${resource}reports-set/?page=${page || 1}`);
  },
  exportReport(id: number) {
    return Repository.get(`${resource}export-report/${id}/`, {
      responseType: 'blob',
      timeout: 30000,
    });
  },
};
