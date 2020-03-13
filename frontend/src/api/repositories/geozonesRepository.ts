import Repository, { baseURL } from '../Repository';

const resource = 'nav-client/geozones-nav/';
const mainResource = `${baseURL}${resource}`;


export default {
  getByName(name: string) {
    return Repository.get(`${resource}?name__contains=${name}`);
  },
};
