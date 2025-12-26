// utils/data-pool.js

// Estado interno por "pool"
const poolIndexes = new Map();

/**
 * Devuelve el siguiente registro del arreglo `records` para el pool dado.
 * Avanza el índice y hace wrap al llegar al final.
 */
export function nextRecord(poolName, records) {
  if (!Array.isArray(records) || records.length === 0) {
    throw new Error(`Data pool vacío para ${poolName}`);
  }

  let idx = poolIndexes.get(poolName) ?? 0;
  const record = records[idx % records.length];
  poolIndexes.set(poolName, idx + 1);
  return record;
}
