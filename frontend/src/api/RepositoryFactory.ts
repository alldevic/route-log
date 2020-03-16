import LoginRepository from './repositories/loginRepository';
import LogoutRepository from './repositories/logoutRepository';
import DevicesRepository from './repositories/devicesRepository';
import ReportsRepository from './repositories/reportsRepository';
import ContainerTypesRepository from './repositories/containerTypesRepository';

type Name = {
  [key: string]: any,
};

const repositories: Name = {
  login: LoginRepository,
  logout: LogoutRepository,
  reports: ReportsRepository,
  devices: DevicesRepository,
  containerTypes: ContainerTypesRepository,
};

const RepositoryFactory = {
  get: (name: string) => repositories[name],
};

export default RepositoryFactory;
