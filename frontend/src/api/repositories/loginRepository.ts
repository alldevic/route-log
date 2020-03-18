import Repository from '../Repository';

const resource = 'auth/token/login/';
export default {
  post(userData: any) {
    return Repository.post(`${resource}`, userData);
  },
};
