import Repository, { baseURL } from '../Repository';

const resource = 'reports/container-types/';
const mainResource = `${baseURL}${resource}`


export default {
    get(page: string) {
        return Repository.get(page ?
            `${mainResource}?page=${page}` :
            `${mainResource}`
        );
    },
};
