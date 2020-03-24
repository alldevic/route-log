import { format } from 'date-fns';

const pattern = 'HH:mm:ss';

export default function dateBeautify(date: any) {
  if (date) {
    return format(new Date(date), pattern);
  }
  return '(n/a)';
}
