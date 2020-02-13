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
  getReport(id: number) {
    return Repository.get(`${resource}${id}/`);
  },
  getContainerUnloads(id: number, page: number) {
    return Repository.get(`${resource}unloads-set/?report=${id}&page=${page || 1}`);
  },
  get() {
    return Repository.get(`${resource}reports-set/`);
  },
};
