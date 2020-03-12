import axios from 'axios';

// const protocol = process.env.VUE_APP_PROTOCOL;
// const domain = process.env.VUE_APP_DOMAIN;
const protocol = 'http';
const domain = 'localhost:8000';

export const baseURL = `${protocol}://${domain}/api/`;
// export const baseURL = `${protocol}://10.10.5.171/`;

const instance = axios.create({
  baseURL: `${baseURL}`,
});

export default instance;
