import Repository, { baseURL } from '../Repository';

const resource = 'nav-client/';

export default {
  getByName(name: string, date: string) {
    if (date) {
      return Repository.get(`${resource}geozones-nav/?name__contains=${name}&date=${date}`);
    }
    return Repository.get(`${resource}geozones-nav/?name__contains=${name}`);
  },
  getMtKey(id: number) {
    return Repository.get(`${resource}geozones-mt/?nav_id=${id}`);
  },
};
