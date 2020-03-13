import LoginRepository from './repositories/loginRepository';
import LogoutRepository from './repositories/logoutRepository';
import DevicesRepository from './repositories/devicesRepository';
import ReportsRepository from './repositories/reportsRepository';
import GeozonesRepository from './repositories/geozonesRepository';

type Name = {
  [key: string]: any,
};

const repositories: Name = {
  login: LoginRepository,
  logout: LogoutRepository,
  reports: ReportsRepository,
  devices: DevicesRepository,
  geozones: GeozonesRepository,
};

const RepositoryFactory = {
  get: (name: string) => repositories[name],
};

export default RepositoryFactory;
