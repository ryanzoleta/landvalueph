import { env } from '$env/dynamic/private';

export async function load() {
  const cities = {
    'CITY OF MANILA': {
      name: 'Manila',
      value: 219000,
      position: { lat: 14.5964947, lng: 120.9883602 },
      color: 'green'
    },
    'CALOOCAN CITY': {
      name: 'Caloocan',
      value: 64200,
      position: { lat: 0, lng: 0 },
      color: 'red'
    },
    'CITY OF LAS PIÑAS': {
      name: 'Las Piñas',
      value: 87500,
      position: { lat: 14.444551, lng: 120.993859 },
      color: 'GREEN'
    },
    'CITY OF MAKATI': {
      name: 'Makati',
      value: 317000,
      position: { lat: 14.55469, lng: 121.024323 },
      color: 'RED'
    },
    'CITY OF MALABON': {
      name: 'Malabon',
      value: 104000,
      position: { lat: 14.668112, lng: 120.965782 },
      color: 'GREEN'
    },
    'CITY OF MANDALUYONG': {
      name: 'Mandaluyong',
      value: 294000,
      position: { lat: 14.579468, lng: 121.035943 },
      color: 'RED'
    },
    'CITY OF MARIKINA': {
      name: 'Marikina',
      value: 77500,
      position: { lat: 14.650766, lng: 121.102913 },
      color: 'GREEN'
    },
    'CITY OF MUNTINLUPA': {
      name: 'Muntinlupa',
      value: 101000,
      position: { lat: 14.407933, lng: 121.041441 },
      color: 'RED'
    },
    'CITY OF NAVOTAS': {
      name: 'Navotas',
      value: 0,
      position: { lat: 14.673315, lng: 120.934692 },
      color: 'GREEN'
    },
    'CITY OF PARAÑAQUE': {
      name: 'Parañaque',
      value: 97700,
      position: { lat: 14.479315, lng: 121.01964 },
      color: 'RED'
    },
    'CITY OF PASIG': {
      name: 'Pasig',
      value: 121000,
      position: { lat: 14.576283, lng: 121.085078 },
      color: 'GREEN'
    },
    'CITY OF SAN JUAN': {
      name: 'San Juan',
      value: 345000,
      position: { lat: 14.601972, lng: 121.035485 },
      color: 'RED'
    },
    'CITY OF VALENZUELA': {
      name: 'Valenzuela',
      value: 59200,
      position: { lat: 0, lng: 0 },
      color: 'GREEN'
    },
    'PASAY CITY': {
      name: 'Pasay',
      value: 122000,
      position: { lat: 14.537701, lng: 121.000859 },
      color: 'RED'
    },
    PATEROS: {
      name: 'Pateros',
      value: 55200,
      position: { lat: 14.545413, lng: 121.068684 },
      color: 'GREEN'
    },
    'QUEZON CITY': {
      name: 'Quezon City',
      value: 128000,
      position: { lat: 14.676137, lng: 121.043606 },
      color: 'RED'
    },
    'TAGUIG CITY': {
      name: 'Taguig',
      value: 234000,
      position: { lat: 14.518043, lng: 121.050857 },
      color: 'GREEN'
    }
  };

  const masterDataDistrict = {};

  return {
    cities,
    MAPS_API_KEY: env.MAPS_API_KEY,
    MAP_ID: env.MAP_ID,
    BARANGAYS_DATASET_ID: env.BARANGAYS_DATASET_ID
  };
}
