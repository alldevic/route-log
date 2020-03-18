import AUTH from '../actions/auth';
import RepositoryFactory from '@/api/RepositoryFactory';
import instance from '@/api/Repository';

const LoginRepository = RepositoryFactory.get('login');
const LogoutRepository = RepositoryFactory.get('logout');

const state = {
  token: localStorage.getItem('user-token') || '',
  status: '',
};

const getters = {
  isAuthenticated: (thisState: any) => !!thisState.token,
  authStatus: (thisState: any) => thisState.status,
};

const actions = {
  async [AUTH.REQUEST]({ commit }: any, user: any) {
    return new Promise(async (resolve) => {
      commit(AUTH.REQUEST);
      const response = await LoginRepository.post(user);
      const token = response.data.auth_token;
      localStorage.setItem('user-token', token);
      instance.defaults.headers.Authorization = `Token ${token}`;
      commit(AUTH.SUCCESS, token);
      resolve(response);
    }).catch((error) => {
      commit(AUTH.ERROR, error);
      localStorage.removeItem('user-token');
    });
  },
  async [AUTH.LOGOUT]({ commit }: any, error: any) {
    return new Promise(async (resolve) => {
      commit(AUTH.LOGOUT);
      if (!error) {
        await LogoutRepository.post();
      }
      localStorage.removeItem('user-token');
      delete instance.defaults.headers.Authorization;
      resolve();
    });
  },
};

const mutations = {
  [AUTH.REQUEST]: (thisState: any) => {
    thisState.status = 'loading';
  },
  [AUTH.SUCCESS]: (thisState: any, thisToken: any) => {
    thisState.status = 'success';
    thisState.token = thisToken;
  },
  [AUTH.ERROR]: (thisState: any) => {
    thisState.status = 'error';
  },
  [AUTH.LOGOUT]: (thisState: any) => {
    thisState.token = '';
  },
};

export default {
  state,
  mutations,
  actions,
  getters,
};
