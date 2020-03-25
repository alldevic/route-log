import Repository, { baseURL } from '../Repository';

const resource = 'nav-client/devices/';
const mainResource = `${baseURL}${resource}`;


export default {
  get({ page, date }: any) {
    return Repository.get(
      mainResource,
      {
        params: {
          page: page ? page : null,
          date
        }
      });
  },
};
