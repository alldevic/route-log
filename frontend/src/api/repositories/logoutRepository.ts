import Repository from '../Repository';

const resource = 'auth/token/logout/';
export default {
  post() {
    return Repository.post(`${resource}`);
  },
};
