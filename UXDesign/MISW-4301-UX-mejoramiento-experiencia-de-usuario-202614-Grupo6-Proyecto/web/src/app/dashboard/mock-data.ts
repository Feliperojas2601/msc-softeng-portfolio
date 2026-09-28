// ============================================================================
// mock-data.ts — Datos hardcodeados para la maqueta navegable del Dashboard.
// No hay llamadas HTTP: todo vive acá para que el componente sea puramente
// visual/interactivo, sin lógica de negocio real.
// ============================================================================

// KPI cards
export type DeltaVariant = 'positivo' | 'neutral';

// KPI cards
export interface KpiCard {
  value: string;
  label: string;
  delta: string;
  deltaVariant: DeltaVariant;
}

// KPI cards
export const KPI_CARDS: KpiCard[] = [
  { value: '5', label: 'Días sin posponer', delta: '↑ 2 vs. semana pasada', deltaVariant: 'positivo' },
  { value: '2', label: 'Snoozes esta semana', delta: '↓ 3 vs. semana pasada', deltaVariant: 'positivo' },
  { value: '92%', label: 'Precisión de metas', delta: '↑ 4 pts', deltaVariant: 'positivo' },
  { value: '1', label: 'Salidas de emergencia', delta: 'Últimos 30 días', deltaVariant: 'neutral' },
];

// Next alarm
export interface DayChip {
  label: string;
  active: boolean;
}

// Next alarm
export const NEXT_ALARM_DAYS: DayChip[] = [
  { label: 'L', active: true },
  { label: 'M', active: true },
  { label: 'X', active: true },
  { label: 'J', active: true },
  { label: 'V', active: true },
  { label: 'S', active: false },
  { label: 'D', active: false },
];

// Recent activity
export type ActivityStatusVariant = 'exito' | 'peligro' | 'acento';

// Recent activity
export interface ActivityItem {
  title: string;
  subtitle: string;
  status: string;
  statusVariant: ActivityStatusVariant;
}

// Recent activity
export const RECENT_ACTIVITY: ActivityItem[] = [
  {
    title: 'Hoy · 06:30',
    subtitle: 'Gym · Reto de escritura',
    status: 'Reto completado',
    statusVariant: 'exito',
  },
  {
    title: 'Ayer · 06:30',
    subtitle: 'Gym · Reto de escritura',
    status: 'Salida de emergencia',
    statusVariant: 'peligro',
  },
  {
    title: 'Lun · 06:30',
    subtitle: 'Gym · Reto de escritura',
    status: 'Pospuesto 2 veces',
    statusVariant: 'acento',
  },
  {
    title: 'Dom · 08:00',
    subtitle: 'Descanso · Sin reto',
    status: 'Reto completado',
    statusVariant: 'exito',
  },
];

// Weekly bar chart
export type WeeklyBarVariant = 'suave' | 'borde' | 'acento';

// Weekly bar chart
export interface WeeklyBar {
  day: string;
  heightPx: number;
  variant: WeeklyBarVariant;
}

// Weekly bar chart
export const WEEKLY_SNOOZES: WeeklyBar[] = [
  { day: 'L', heightPx: 44, variant: 'suave' },
  { day: 'M', heightPx: 6, variant: 'borde' },
  { day: 'X', heightPx: 88, variant: 'suave' },
  { day: 'J', heightPx: 44, variant: 'suave' },
  { day: 'V', heightPx: 6, variant: 'borde' },
  { day: 'S', heightPx: 132, variant: 'acento' },
  { day: 'D', heightPx: 44, variant: 'suave' },
];

// User
export interface MockUser {
  initials: string;
  name: string;
  email: string;
}

// User
export const CURRENT_USER: MockUser = {
  initials: 'PA',
  name: 'Paula Alarcón',
  email: 'paula.abc@gmail.com',
};
